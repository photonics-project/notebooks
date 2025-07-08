SOURCES := $(filter-out ./src/controls.py, $(wildcard ./src/*.py))
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

.PHONY: all
all: lowtran notebooks

.PHONY: build
build: all | ./build/
	cp ./lowtran/lowtran7.npz ./build/
	cp ./src/controls.py ./build/
	cp -r ./src/templates ./build/

.PHONY: lowtran
lowtran:
	make -C lowtran

.PHONY: notebooks
notebooks: $(NOTEBOOKS)

.PHONY: check
check: build
	pytest --nbmake ./build/

.PHONY: start-dev
start-dev: stop-dev build
	watchmedo shell-command ./src/ --recursive --patterns="*.py;*.vue" --command='make build' \
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
	- rm -rf ./build

.PHONY: clean-all
clean-all: clean
	make clean -C lowtran

./build/:
	mkdir -p ./build

./build/%.ipynb: ./src/%.py | ./build/
	jupytext --from py:percent --to notebook --output $@ $<
