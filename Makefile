.PHONY: all

all: figures/single_wb.png figures/floodplain.png

figures/single_wb.png: figures/single_wb.py
	python $<

figures/floodplain.png: figures/floodplain.py
	python $<
