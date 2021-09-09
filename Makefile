SOURCES := $(wildcard *.py)
NOTEBOOKS := $(patsubst %.py,%.ipynb,$(SOURCES))


.PHONY: default
default: help

.PHONY: help
help:
	@echo
	@echo "Photonics Project Notebooks"
	@echo "==========================="
	@echo "Below are the available \`make\` targets for the Photoics Project Notebooks package."
	@echo
	@echo "Development:"
	@echo "  install-requirements"
	@echo "    install the requirements in the current Python environment"
	@echo "  start-dev"
	@echo "    watch Python source files and convert to IPython notebooks"
	@echo "    run Voila server"
	@echo "  stop-dev"
	@echo "    terminate the background processes initiated by \`start-dev\`"
	@echo

.PHONY: install-requirements
install-requirements:
	$(MAKE) -C ./requirements/ install

.PHONY: notebooks
notebooks: $(NOTEBOOKS)

.PHONY: start-dev
start-dev: stop-dev $(NOTEBOOKS)
	watchmedo shell-command \
		--patterns="*.py" \
		--command='jupytext --from py:percent --to notebook $${watch_src_path}' \
		& echo "$$!" >> watchmedo.pid
	voila --debug . & echo "$$!" >> voila.pid

.PHONY: stop-dev
stop-dev:
	- pkill -F watchmedo.pid
	- pkill -F voila.pid
	- rm watchmedo.pid
	- rm voila.pid

.PHONY: clean
clean:
	- rm *.ipynb

%.ipynb: %.py
	jupytext --from py:percent --to notebook $<
