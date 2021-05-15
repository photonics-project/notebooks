.PHONY: default
default: lowtran7 data

lowtran7:
	gfortran -std=legacy lowtran7.f -o lowtran7

.PHONY: data
data: lowtran7
	python lowtran7.py
	./lowtran7
	python lowtran7.py post-process

.PHONY: clean
clean:
	- rm *.npz
	- rm *.o
	- rm lowtran7
	- rm TAPE*
