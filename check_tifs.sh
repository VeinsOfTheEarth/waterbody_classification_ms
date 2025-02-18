#!/bin/bash
# print any workspace folders without tif files

# gnu find
find data -type d -regextype egrep -regex '.*/[0-9]{7}' > data_folders.txt

# # macos
# find -E data -iregex '.*[0-9]{7}' > data_folders.txt

for folder in `cat data_folders.txt`
do
    if [ ! -d "$folder/data/tif" ]; then
        echo "$folder does not exist."
    fi    
done
