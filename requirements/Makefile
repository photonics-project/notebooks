.PHONY: default
default: all install

.PHONY: all
all: requirements.txt dev-requirements.txt ../binder/requirements.txt

.PHONY: install
install: requirements.txt dev-requirements.txt
	pip-sync $^

dev-requirements.txt: dev-requirements.in requirements.txt
	pip-compile $<

../binder/requirements.txt: requirements.in requirements.txt
	cat requirements.in | xargs -I{} sed -n '/^{}==/p' requirements.txt > $@

%.txt: %.in
	pip-compile $<
