import argparse
import sys
from importlib import import_module
from pathlib import Path
import os
import subprocess
import csv
from shutil import rmtree, make_archive, copy

import requests
import pandas as pd
from git import Repo

from pfb.reader import PFBReader
from pfb.exporters import tsv
from dictionaryutils.utils import node_values_to_codes



class Config():
    def __init__(self):
        self.reader = None



class PFBExporter:
    def __init__(self, pfb_file_path:str, tmp_folder:str, output_path:str, config_file_path:str, ontology:str=None, extra_analysis:str=None) -> None:
        self.pfb_file_path = pfb_file_path
        self.tmp_folder = tmp_folder if tmp_folder else "./tmp"
        self.output_path = output_path if output_path else "./"
        self.ontology = ontology
        self.analysis_path = extra_analysis
        self.zip_file_output_path = None

        # Retrieve config file module
        path, file = config_file_path.rsplit('/', 1)
        file = file[:-3]
        sys.path.append(path)
        self.config = import_module(file)

        self.data_dictionary = None
        if self.ontology and self.ontology == "ncit":
            response = requests.get(self.config.data_dictionary)
            if response.status_code != 200:
                print("ERROR retrieving data dictionary!!!!!")
                print(response.text)
                exit()
            self.data_dictionary = response.json()

        self.pfb_file = None
        self.reader = None
        self.zip_folder = None
        

    @classmethod
    def _validate(cls, *args, **kwargs):
        if not args: 
            print(args)
            print(list(kwargs.keys()))
            return False

        path = Path(args[0])
        if not path.is_file():
            print(f"File {args[0]} is not found.")
            return False

        return True

    def __new__(cls, *args, **kwargs):
        if cls._validate(*args, **kwargs):
            return super().__new__(cls)

        

    def initialize(self):
        print("Initializing...")
        # Initialize PFB reader
        self.pfb_file = open(self.pfb_file_path, 'rb')
        if self.pfb_file:
            self.reader = PFBReader(self.pfb_file)
        else:
            print("problem opening the avro file")
            return None

        # Initialize tmp folder
        tmp_path = Path(self.tmp_folder)
        if not tmp_path.exists():
            tmp_path.mkdir()
            print(f"Temporary data directory is created at {self.tmp_folder}")

        source = self.pfb_file_path
        filename_with_ext = source.split("/")[-1]
        filename_without_ext = filename_with_ext.split('.')[-2]
        self.zip_folder = self.tmp_folder + "/" + filename_without_ext
        self.zip_subfolder = filename_without_ext

        tmp_path = Path(self.zip_folder)
        if not tmp_path.exists():
            tmp_path.mkdir()
            print(f"Temporary data directory is created at {self.tmp_folder + '/zip'}")

        # # Add avro/PFB file to the zip folder
        # copy(self.pfb_file_path, self.zip_folder + "/" + filename_with_ext)

        # Create tsvs subforlders
        tmp_path = Path(self.zip_folder + "/tsvs")
        if not tmp_path.exists():
            tmp_path.mkdir()

        tmp_path = Path(self.zip_folder + "/tsvs_original")
        if not tmp_path.exists():
            tmp_path.mkdir()

        if self.ontology:
            tmp_path = Path(self.zip_folder + "/tsvs_codes")
            if not tmp_path.exists():
                tmp_path.mkdir()

        if self.analysis_path:
            tmp_path = Path(self.zip_folder)
            self.analysis_path = str(tmp_path.resolve())
            tmp_path = Path(self.analysis_path + "/analysis")
            if not tmp_path.exists():
                tmp_path.mkdir()

            tmp_path = os.path.join("./", "repo")
            if Path(tmp_path).exists():
                rmtree(tmp_path, ignore_errors=False, onerror=None)

            repo = Repo.clone_from("https://github.com/chicagopcdc/pcdc_analysis_scripts.git", tmp_path, branch="main") #self.tmp_folder


    def export(self):
        self.reader = self.reader.__enter__()
        exclude_file = self.config.exclude_files if self.config.exclude_files and len(self.config.exclude_files) > 0 else None
        tsv._to_tsv(self.reader, self.zip_folder + "/tsvs_original", {}, exclude_file)


    def filter_attributes(self, is_black_list=False):
        '''Takes as argument 
        a list of attributes to whitelist, by default, and a black_list
        boolean to indicate if the list of attributes should be blacklisted instead.
        '''
        attribute_list = self.config.black_list if is_black_list else self.config.white_list

        for file in os.listdir(self.zip_folder + "/tsvs_original"):
            if file.split(".")[0] in attribute_list.keys():
                print("Filtering " + file + " ...")
                with open(os.path.join(self.zip_folder + "/tsvs_original", file), 'r') as f_read:
                    reader = csv.reader(f_read, delimiter='\t')
                    header = next(reader)
                    if is_black_list:
                        filtered_header = [
                            attribute 
                            for attribute in header 
                            if attribute not in attribute_list[file.split(".")[0]]
                        ]
                    else:
                        filtered_header = [
                            attribute 
                            for attribute in header 
                            if attribute in attribute_list[file.split(".")[0]]
                        ]

                    with open(os.path.join(self.zip_folder + "/tsvs", file), 'w') as f_write:
                        writer = csv.writer(f_write, delimiter='\t')
                        writer.writerow(filtered_header)
                        for row in reader:
                            filtered_row = [
                                value 
                                for attribute, value in zip(header, row) 
                                if attribute in filtered_header
                            ]
                            writer.writerow(filtered_row)
            else:
                print(file + " NOT FILTERED, no config is present for it.")
                # just copy it over to the filtered folder
                copy(self.zip_folder + "/tsvs_original/" + file, self.zip_folder + "/tsvs/" + file)

    
    # TODO not working need to be updated
    def filtered_attributes_pd(self, output_directory=None, is_black_list=False):
        '''Takes as argument a directory containing several TSV files,
        a list of attributes to whitelist, by default, and a black_list
        boolean to indicate if the list of attributes should be blacklisted instead.
        '''

        attribute_list = self.config.black_list if is_black_list else self.config.white_list

        for file in os.listdir(self.zip_folder + "/tsvs_original"):
            if not file.endswith('.tsv'):
                continue
            df = pd.read_csv(os.path.join(self.zip_folder + "/tsvs_original", file), sep='\t')

            headers = [
                attribute
                for attribute in df.columns
                if attribute in attribute_list
            ]
            if is_black_list:
                df.drop(headers)
            else:
                df = df[headers]
            if not output_directory:
                output_directory = self.zip_folder + "/tsvs_original"
            df.to_csv(os.path.join(output_directory, file), sep='\t', index=False)


    def to_ontology_code(self):
        if not self.ontology:
            print("No ontology selected")
            return

        for file in os.listdir(self.zip_folder + "/tsvs"):
            key = file.split(".")[0]
            if key not in self.data_dictionary or not self.data_dictionary[key]:
                print(key + " NOT PRESENT in data dictionary")
                copy(self.zip_folder + "/tsvs/" + file, self.zip_folder + "/tsvs_codes/" + file)
                continue

            print("Translating " + file + " from values to " + self.ontology + " codes...")

            with open(os.path.join(self.zip_folder + "/tsvs", file), 'r') as f_read:
                reader = csv.reader(f_read, delimiter='\t')
                header = next(reader)
                with open(os.path.join(self.zip_folder + "/tsvs_codes", file), 'w') as f_write:
                    writer = csv.writer(f_write, delimiter='\t')
                    writer.writerow(header)
                    for row in reader:
                        translated_row = [
                            value 
                            for attribute, value in node_values_to_codes(self.data_dictionary[key], list(zip(header, row)), self.ontology) 
                        ]
                        writer.writerow(translated_row)

        rmtree(self.zip_folder + "/tsvs", ignore_errors=False, onerror=None)


    def setup_and_run_analysis(self, consortium=None):
        if not self.analysis_path:
            print("No analysis_path selected")
            return

        # TODO check consortiums exists and there is relevant scripts for it
        if not consortium:
            print("No consortium parameter found!")
            return

        # TODO check R is installed
        try:
            command = 'which RScript'
            cmd_output = subprocess.check_output(command, shell=True, text=True).rstrip('\n')
        except subprocess.CalledProcessError as grepexc:
            print("error code", grepexc.returncode, grepexc.output)
            print("R is not installed / not found!")
            return

        current_dir = str(Path( __file__ ).parent.absolute())
        # subprocess.call(cmd_output + " --vanilla ./repo/INRG/PCDC_To_INRG_Data_Transformation.R", shell=True)
        subprocess.call ([cmd_output, "--vanilla", "./repo/INRG/PCDC_To_INRG_Data_Transformation.R", os.path.join(current_dir, "repo/"), self.analysis_path + "/tsvs/", self.analysis_path + "/analysis/"])


        # TODO cd to consortia subfolder
        # TODO run the script with the input and output parameters
        return None
   

    def zip(self):
        # Clean pre-filtered TSVs
        rmtree(self.zip_folder + "/tsvs_original", ignore_errors=False, onerror=None)

        # output_filename = self.pfb_file_path
        output_filename = self.output_path + self.zip_folder.split("/")[-1]
        self.zip_file_output_path = make_archive(output_filename, 'zip', self.tmp_folder, self.zip_subfolder)
        print(f"ZIP file created at {self.zip_file_output_path}")


    def clean_up(self):
        print(f"Removing all the resources used and the temporary data directory at {self.tmp_folder}")

        try:
            self.pfb_file.close()
        except:
            print("something went wrong during clean up")

        try:
            # Remove all the files in self.tmp_folder and the directory itself
            rmtree(self.tmp_folder, ignore_errors=False, onerror=None)
            tmp_path = os.path.join("./", "repo")
            if Path(tmp_path).exists():
                rmtree(tmp_path, ignore_errors=False, onerror=None)
        except FileNotFoundError as e:
            print(e)





def main():
    # EXAMPLE: python pfb_to_zip.py -i ./export_2023-03-27T02_42_17.avro -o ./outputs/ -c ./config.py -d https://portal.pedscommons.org/api/v0/submission/_dictionary/_all -t ncit

    parser = argparse.ArgumentParser(description="Build ZIP bundle for data delivery after project request has been approved")
    parser.add_argument('-c', '--config', help='The config file')
    parser.add_argument('-i', '--input', help='Input PFB file path')
    parser.add_argument('-o', '--output', help='Output ZIP directory')
    parser.add_argument('-t', '--terminology', help='The ontology you want to transform GEN3 values to.')
    parser.add_argument('-a', '--analysis', help='The consorti script you want to execute. Ex:INRG')

    try:
        args = parser.parse_args()
        input_path = args.input
        output_path = args.output
        config_file = args.config
        ontology = args.terminology
        analysis_script_consortia = args.analysis
    except argparse.ArgumentError as err:
        print(err)
        parser.print_help()


    tmp_folder = "./tmp"
    pfb_export = PFBExporter(input_path, tmp_folder, output_path, config_file, ontology, True if analysis_script_consortia and analysis_script_consortia != "" else False)
    if not pfb_export:
        print("One or more problems occurred during the initialization of the PFBExporter class")
        exit()

    pfb_export.initialize()
    pfb_export.export()
    pfb_export.filter_attributes(is_black_list=False)
    # pfb_export.filter_attributes(is_black_list=True)
    pfb_export.setup_and_run_analysis(analysis_script_consortia) #TODO how to find consortium
    pfb_export.to_ontology_code() 
    pfb_export.zip()
    pfb_export.clean_up()

    



if __name__ == "__main__":
    main()


