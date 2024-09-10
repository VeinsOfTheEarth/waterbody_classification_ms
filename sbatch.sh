#!/bin/bash

#Submit this script with: sbatch filename
# sbatch -J 0770110 sbatch.sh 0770110

##SBATCH --time=0:2:00   # walltime
#SBATCH --output=data/%x/%j   # output file name
#SBATCH --qos=normal   # qos name
#SBATCH --partition=general   # partition name

module load miniconda3
source activate planet
which python
# make data_eval
make test gpkgs="data/$1/data/wb_all.gpkg"
make data_eval gpkgs="data/$1/data/wb_all.gpkg"
# make clean
rm -rf data/$1/data/tifs 
