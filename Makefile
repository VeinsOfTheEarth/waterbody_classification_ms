.PHONY: all manuscript figures data_eval test data

PDFCROP=pdfcrop.pl
gpkgs ?= $(addprefix data/, $(addsuffix /data/wb_all.gpkg, $(shell cat data/aois.txt)))
populates ?= $(addprefix data/, $(addsuffix /query_ids_quality.txt, $(shell cat to_transfer.txt)))
preflights ?= $(addprefix data/, $(addsuffix /query_ids_quality.txt, $(shell cat preflight.txt)))

all: manuscript figures data

data: data/cubeSat_buffered_mask_tiles.gpkg

data/cubeSat_buffered_mask_tiles.gpkg: data/CubeSat_Arctic_Boreal_LakeArea_1667/data/CubeSat_Buffered_Mask_Tiles.kmz
	ogr2ogr $@ $<

# this target is meant to be called manually, kicks off full pipeline
data_eval: $(gpkgs)

$(gpkgs): data/aois.txt
	@echo $(firstword $(subst /data, ,$(@D)))
	@echo $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D)))))
	@echo $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D))))))
	#
	wbpopulate \
	--folder $(firstword $(subst /data, ,$(@D))) \
	--tag $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D))))) \
	--aoi $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D)))))) \
	--model $(HOME)/python/torchwbtype/torchwbtype/data
	#
	wbrun --folder $(firstword $(subst /data, ,$(@D)))
	wbrun --folder $(firstword $(subst /data, ,$(@D)))

# --- for workflows where the Planet API is not available, and
#		data is staged from elsewhere
populate:
	wbpopulate --folder data/$(AOI_NUMBER) --tag $(AOI_NUMBER) --aoi data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_$(AOI_NUMBER).tif --model $(HOME)/python/torchwbtype/torchwbtype/data

populates_eval: $(populates)

$(populates): to_transfer.txt
	@echo $(firstword $(subst /data, ,$(@D)))
	@echo $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D)))))
	@echo $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D))))))
	#
	wbpopulate \
	--folder $(firstword $(subst /data, ,$(@D))) \
	--tag $(subst data/, , $(subst /data, , $(firstword $(subst /data, ,$(@D))))) \
	--aoi $(addsuffix .tif, $(addprefix data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_, $(subst /data, , $(firstword $(subst data/, ,$(@D)))))) \
	--model $(HOME)/python/torchwbtype/torchwbtype/data

preflight:
	make -B -f data/$(AOI_NUMBER)/Makefile query_ids_quality_eval

preflights_eval: $(preflights)

$(preflights): to_transfer.txt
	make -B -f data/$(subst data/,,$(subst /data,,$(firstword $(subst /data,,$(@D)))))/Makefile query_ids_quality_eval

# ---

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
	-@rm *.out
	-@python -c "import os; import shutil; import re; [shutil.rmtree(f) for f in os.listdir('.') if re.search(r'.{8}-.{4}', f) is not None];"
	-@rm mask*.tif
	-@rm res_sum*.tif
	-@rm recurrence*.gpkg

install:
	pip install --upgrade -e $(HOME)/python/wbextractor
