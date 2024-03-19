.PHONY: all manuscript figures

all: manuscript figures

manuscript: manuscript/manuscript.pdf

figures: figures/single_wb.pdf figures/floodplain.pdf figures/study_site.pdf

figures/single_wb.pdf: figures/single_wb.py
	python $<

figures/floodplain.pdf: figures/floodplain.py
	python $<

figures/study_site.pdf: figures/study_site.py
	python $<

figures/table_image-list.pdf: figures/table_image-list.py scripts/utils.py
	python $<
	pdfcrop $@ $@

figures/table_metric-list.pdf: figures/table_metric-list.py scripts/utils.py
	python $<
	pdfcrop $@ $@

manuscript: manuscript/manuscript.pdf manuscript/supplement.pdf

manuscript/manuscript.pdf: manuscript/manuscript.tex manuscript/riverlakeid.bib
	cd manuscript && pdflatex manuscript.tex
	cd manuscript && bibtex manuscript
	cd manuscript && bibtex manuscript
	cd manuscript && pdflatex manuscript.tex

manuscript/supplement.pdf: manuscript/supplement.tex
	cd manuscript && pdflatex supplement.tex
