.PHONY: all manuscript figures

all: manuscript figures

manuscript: manuscript/manuscript.pdf

figures: figures/single_wb.pdf figures/floodplain.pdf

figures/single_wb.pdf: figures/single_wb.py
	python $<

figures/floodplain.pdf: figures/floodplain.py
	python $<

manuscript: manuscript/manuscript.pdf

manuscript/manuscript.pdf: manuscript/manuscript.tex manuscript/riverlakeid.bib
	cd manuscript && pdflatex manuscript.tex
	cd manuscript && bibtex manuscript
	cd manuscript && bibtex manuscript
	cd manuscript && pdflatex manuscript.tex
