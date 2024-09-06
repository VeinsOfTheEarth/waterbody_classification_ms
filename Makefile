.PHONY: all manuscript figures data_eval test

PDFCROP=pdfcrop.pl
gpkgs := $(addprefix data/, $(addsuffix /data/wb_all.gpkg, $(shell cat data/aois.txt)))

test:
	@echo $(gpkgs)

all: manuscript figures data_eval

data_eval: $(gpkgs)

$(gpkgs): 
	@echo $(firstword $(subst /data, ,$(@D)))
	@echo $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D)))))
	@echo $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D))))))
	#
	wbpopulate \
	--folder $(firstword $(subst /data, ,$(@D))) \
	--tag $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D))))) \
	--aoi $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D)))))) \
	--model /vast/home/jsta/python/torchwbtype/torchwbtype/data
	#
	wbrun --folder $(firstword $(subst /data, ,$(@D)))
	wbrun --folder $(firstword $(subst /data, ,$(@D)))
	
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

clean:
	-@rm core.*
	-@python -c "import os; import shutil; import re; [shutil.rmtree(f) for f in os.listdir('.') if re.search(r'.{8}-.{4}', f) is not None];"
