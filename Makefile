.PHONY: all manuscript figures data

PDFCROP=pdfcrop.pl
gpkgs := $(addsuffix /data/wb_all.gpkg, $(shell cat data/aois.txt))

all: manuscript figures data

# echo $(firstword $(subst /, ,$(<D)))
data_eval: $(gpkgs)

$(gpkgs): data/aois.txt
	@echo $(addprefix data/, $(firstword $(subst /, ,$(@D))))
	@echo $(firstword $(subst /, ,$(@D)))
	@echo $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(firstword $(subst /, ,$(@D)))))
	wbpopulate \
	--folder $(addprefix data/, $(firstword $(subst /, ,$(@D)))) \
	--tag $(firstword $(subst /, ,$(@D))) \
	--aoi $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(firstword $(subst /, ,$(@D))))) \
	--model /vast/home/jsta/python/torchwbtype/torchwbtype/data
	#
	wbrun --folder $(addprefix data/, $(firstword $(subst /, ,$(@D)))) --target csvs
	
manuscript: manuscript/manuscript.pdf figures

figures: figures/single_wb.pdf figures/floodplain.pdf figures/study_site.pdf figures/table_image-list.pdf

figures/single_wb.pdf: figures/single_wb.py
	python $<

figures/floodplain.pdf: figures/floodplain.py
	python $<

figures/study_site.pdf: figures/study_site.py
	python $<

figures/table_image-list.pdf: figures/table_image-list.py scripts/utils.py
	python $<
	$(PDFCROP) $@ $@

figures/table_metric-list.pdf: figures/table_metric-list.py scripts/utils.py
	python $<
	$(PDFCROP) $@ $@

manuscript: manuscript/combined.pdf

manuscript/combined.pdf: manuscript/manuscript.pdf manuscript/supplement.pdf
	pdftk manuscript/manuscript.pdf manuscript/supplement.pdf cat output $@


manuscript/manuscript.pdf: manuscript/manuscript.tex manuscript/hydroml_2023.bib
	cd manuscript && pdflatex manuscript.tex
	cd manuscript && bibtex manuscript
	cd manuscript && bibtex manuscript
	cd manuscript && pdflatex manuscript.tex

manuscript/supplement.pdf: manuscript/supplement.tex
	cd manuscript && pdflatex supplement.tex
