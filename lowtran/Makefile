.PHONY: default
default: lowtran7 data

.PHONY: data
data: lowtran7.npz

.PHONY: clean
clean:
	- rm *.npz
	- rm *.o
	- rm lowtran7
	- rm TAPE*

lowtran7: lowtran7.f
	gfortran -std=legacy lowtran7.f -o lowtran7

TAPE5: lowtran7.py
	python lowtran7.py prepare-TAPE5

TAPE7: lowtran7 TAPE5
	./lowtran7

lowtran7.npz: TAPE7 lowtran7.py
	python lowtran7.py process-TAPE7
