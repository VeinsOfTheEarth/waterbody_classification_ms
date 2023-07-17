.PHONY: all manuscript

all: figures/single_wb.png figures/floodplain.png

figures/single_wb.png: figures/single_wb.py
	python $<

figures/floodplain.png: figures/floodplain.py
	python $<

manuscript: manuscript/manuscript.pdf

manuscript/manuscript.pdf: manuscript/manuscript.tex manuscript/riverlakeid.bib
	cd manuscript && pdflatex manuscript.tex
	cd manuscript && bibtex manuscript
	cd manuscript && bibtex manuscript
	cd manuscript && pdflatex manuscript.tex
