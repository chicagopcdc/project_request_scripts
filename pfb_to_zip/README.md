# Description
Extract PFB to a TSVs, with the ability to filter by column, filter by filter by file, and transform term and values to ontology codes when present.

# Requirements
R and R Studio need to be installed for the INRG transformation to work. You can download them (here)[https://posit.co/download/rstudio-desktop/]

# Usage
python pfb_to_zip.py -i ./export_2023-03-27T02_42_17.avro -o ./outputs/ -c ./config.py -t ncit

`-i` the input PFB/AVRO file
`-o` the output folder path
`-c` the config file
`-t` ontology you want to transform the values to
`-a` for extra INRG analysis 




python pfb_to_zip.py -i ./INRG_2024_02_20240923.avro -o ./outputs/ -c ./config.py -a INRG 