.PHONY: default
default: all install

.PHONY: all
all: requirements.txt dev-requirements.txt

.PHONY: install
install: requirements.txt dev-requirements.txt
	pip-sync $^

dev-requirements.txt: dev-requirements.in requirements.txt
	pip-compile $<

%.txt: %.in
	pip-compile $<
