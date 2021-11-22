SOURCES := $(wildcard ./src/*.py)
NOTEBOOKS := $(patsubst ./src/%.py,./build/%.ipynb,$(SOURCES))


.PHONY: default
default: help

.PHONY: help
help:
	@echo
	@echo "Photonics Project Notebooks"
	@echo "==========================="
	@echo "Below are the available \`make\` targets for the Photoics Project Notebooks package."
	@echo
	@echo "Build:"
	@echo "  install-requirements"
	@echo "    install the requirements in the current Python environment"
	@echo "  lowtran"
	@echo "    compile and run lowtran to construct the data tables"
	@echo "  notebooks"
	@echo "    build the notebooks"
	@echo
	@echo "Development:"
	@echo "  start-dev"
	@echo "    watch Python source files and convert to IPython notebooks"
	@echo "    run Voila server"
	@echo "  stop-dev"
	@echo "    terminate the background processes initiated by \`start-dev\`"
	@echo

.PHONY: install-requirements
install-requirements:
	$(MAKE) -C ./requirements/ install

.PHONY: all
all: lowtran notebooks

.PHONY: lowtran
lowtran:
	make -C lowtran
	mkdir -p ./build/lowtran/
	cp ./lowtran/lowtran7.npz ./build/lowtran

.PHONY: notebooks
notebooks: $(NOTEBOOKS) lowtran ./build/controls.py

.PHONY: check
check: notebooks
	pytest --nbmake ./build/

.PHONY: start-dev
start-dev: stop-dev notebooks
	watchmedo shell-command ./src/ --patterns="*.py" --command='make notebooks' \
	  & echo "$$!" >> watchmedo.pid
	voila --debug ./build/ \
	  & echo "$$!" >> voila.pid

.PHONY: stop-dev
stop-dev:
	- pkill -F watchmedo.pid
	- pkill -F voila.pid
	- rm watchmedo.pid
	- rm voila.pid

.PHONY: clean
clean:
	- rm -rf ./build/*

.PHONY: clean-all
clean-all: clean
	make clean -C lowtran

./build/controls.py: ./src/controls.py
	cp $< $@

./build/%.ipynb: ./src/%.py
	mkdir -p ./build/
	jupytext --from py:percent --to notebook --output $@ $<
