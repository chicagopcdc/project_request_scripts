import argparse
from pathlib import Path
import os
import re
import subprocess
import csv
import json
from shutil import rmtree, make_archive, copy, copytree

import requests
import pandas as pd
from git import Repo

from pfb.reader import PFBReader
from pfb.exporters import tsv
from dictionaryutils.utils import node_values_to_codes
from pfb.writer import PFBWriter

from db_config import get_api_config, load_config, load_config_module


def to_folder_name(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = value.strip("_")
    return value


class Config():
    def __init__(self):
        self.reader = None

class PFBExporter:
    def __init__(
        self,
        pfb_file_path: str,
        tmp_folder: str,
        output_path: str,
        config_file_path: str,
        ontology: str = None,
        extra_analysis: str = None,
        project_id: int = None,
        api_config: dict = None,
    ) -> None:
        self.pfb_file_path = pfb_file_path
        self.tmp_folder = tmp_folder if tmp_folder else "./tmp"
        self.output_path = output_path if output_path else "./"
        self.ontology = ontology
        self.analysis_path = extra_analysis
        self.zip_file_output_path = None

        fallback_config = load_config_module(config_file_path)
        if project_id is not None:
            self.config, self.config_source = load_config(
                project_id, api_config or get_api_config(), fallback_config
            )
        else:
            self.config = fallback_config
            self.config_source = "Config source: local file (--project-id not set)"

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
                rmtree(tmp_path, ignore_errors=False, onexc=None)

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
        invalid_attributes = {}
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
                        invalid_attributes[file.split(".")[0]] = [
                            a for a in attribute_list[file.split(".")[0]] if a not in header
                        ]
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
        if any(a for a in invalid_attributes.values()):
            raise RuntimeError(f'Invalid attributes in config: {({k:v for k,v in invalid_attributes.items() if v})}')

    
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
   

    def add_external_references_material(self):
        external_references_path = self.zip_folder + "/tsvs/external_reference.tsv"
        resources_set = set()

        if Path(external_references_path).exists():
            with open(external_references_path, "r", encoding="utf-8") as f_read:
                reader = csv.reader(f_read, delimiter="\t")
                header = next(reader)

                # find column index
                try:
                    idx = header.index("external_resource_name")
                except ValueError:
                    print("external_resource_name column not found")
                    return

                for row in reader:
                    if len(row) > idx and row[idx]:
                        resources_set.add(row[idx])

        if resources_set:
            tmp_path = Path(self.zip_folder) / "external_references_information"
            tmp_path.mkdir(exist_ok=True)

            for item in resources_set:
                item_normalized = to_folder_name(item)
                src = Path("templates") / item_normalized
                dst = tmp_path / item_normalized

                if src.exists():
                    copytree(src, dst, dirs_exist_ok=True)
                else:
                    print(f"Template not found: {src}")


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


class Difference:
    def __init__(self, old_file_path: str, new_file_path: str):
        self.old_file = old_file_path
        self.new_file = new_file_path

    def read_avro(self, file_path):
        records_by_subject = {}

        with open(file_path, 'rb') as f:
            with PFBReader(f) as reader:
                for record in reader:
                    obj = record['object']
                    name = record['name']

                    if name == 'subject':
                        sid = obj.get('submitter_id')
                    else:
                        sid = obj.get('subjects.submitter_id')

                    if sid:
                        if sid not in records_by_subject:
                            records_by_subject[sid] = {}
                        if name not in records_by_subject[sid]:
                            records_by_subject[sid][name] = []
                        records_by_subject[sid][name].append(record)

        return records_by_subject

    # removes created and updated times from data for comparison
    def _strip_timestamps(self, nodes):
        stripped = {}
        for node_name, records in nodes.items():
            stripped[node_name] = []
            for r in records:
                stripped_record = r.copy()
                obj = r['object'].copy()
                obj.pop('created_datetime', None)
                obj.pop('updated_datetime', None)
                stripped_record['object'] = obj
                stripped[node_name].append(stripped_record)
        return stripped

    def _normalize(self, nodes):
        normalized = self._strip_timestamps(nodes)
        for node_name in normalized:
            normalized[node_name] = sorted(
                normalized[node_name],
                key=lambda r: json.dumps(r, sort_keys=True)
            )
        return normalized

    def generate_diff(self, output_path: str):
        old = self.read_avro(self.old_file)
        new = self.read_avro(self.new_file)

        deleted_sids = set(old.keys()) - set(new.keys())
        diff_records = []
        log_lines = []

        if deleted_sids:
            msg = f"{len(deleted_sids)} subject(s) removed:"
            print(msg)
            log_lines.append(msg)
            for sid in sorted(deleted_sids):
                line = f"   - {sid}"
                print(line)
                log_lines.append(line)
                for records in old[sid].values():
                    for record in records:
                        line = f"     - {record['name']}: {record['object']}"
                        print(line)
                        log_lines.append(line)
        else:
            msg = "No subjects removed."
            print(msg)
            log_lines.append(msg)

        for sid, new_nodes in new.items():
            if sid not in old:
                for records in new_nodes.values():
                    diff_records.extend(records)
            else:
                if self._normalize(new_nodes) != self._normalize(old[sid]):
                    for records in new_nodes.values():
                        diff_records.extend(records)

        summary = f"Total changed/new records in diff: {len(diff_records)}"
        print(summary)
        log_lines.append(summary)

        log_path = output_path.replace('.avro', '_log.md')
        with open(log_path, 'w') as f:
            f.write("# Diff Log\n\n")
            f.write("\n".join(log_lines))

        with open(output_path, 'wb') as out_f:
            with PFBWriter(out_f) as writer:
                with open(self.new_file, 'rb') as schema_f:
                    with PFBReader(schema_f) as reader:
                        writer.copy_schema(reader)
                writer.write(diff_records)

        print(f"Written to {output_path} with {len(diff_records)} records")

def main():
    # EXAMPLE: python pfb_to_zip.py -i ./export_2023-03-27T02_42_17.avro -o ./outputs/ -c ./config.py -d https://portal.pedscommons.org/api/v0/submission/_dictionary/_all -t ncit
    # Example for diff: python3 pfb_to_zip.py -i ../new_data.avro -o ../outputs/ -c ./config.py -d ../old_data.avro

    parser = argparse.ArgumentParser(description="Build ZIP bundle for data delivery after project request has been approved")
    parser.add_argument('-c', '--config', help='Fallback config file (exclude_files, data_dictionary, and white/black lists if API unavailable)')
    parser.add_argument('-p', '--project-id', type=int, help='Load white_list and black_list from amanuensis project_datapoints for this project')
    parser.add_argument('--amanuensis-url', default=os.environ.get('AMANUENSIS_URL', 'https://localhost'), help='Portal base URL (default: AMANUENSIS_URL or https://localhost)')
    parser.add_argument('--access-token', default=os.environ.get('AMANUENSIS_ACCESS_TOKEN'), help='Bearer token with amanuensis access (default: AMANUENSIS_ACCESS_TOKEN env var)')
    parser.add_argument('-i', '--input', help='Input PFB file path')
    parser.add_argument('-o', '--output', help='Output ZIP directory')
    parser.add_argument('-t', '--terminology', help='The ontology you want to transform GEN3 values to.')
    parser.add_argument('-a', '--analysis', help='The consorti script you want to execute. Ex:INRG')
    parser.add_argument('-d', '--diff', help='Path to the old avro file to diff against')

    try:
        args = parser.parse_args()
        input_path = args.input
        output_path = args.output
        config_file = args.config
        project_id = args.project_id
        api_config = get_api_config(
            base_url=args.amanuensis_url,
            token=args.access_token,
        )
        ontology = args.terminology
        analysis_script_consortia = args.analysis
    except argparse.ArgumentError as err:
        print(err)
        parser.print_help()

    if args.diff:
        diff = Difference(args.diff, input_path)
        diff_output = output_path + 'diff.avro'
        diff.generate_diff(diff_output)
        input_path = diff_output

    tmp_folder = "./tmp"
    pfb_export = PFBExporter(
        input_path,
        tmp_folder,
        output_path,
        config_file,
        ontology,
        True if analysis_script_consortia and analysis_script_consortia != "" else False,
        project_id=project_id,
        api_config=api_config,
    )
    if not pfb_export:
        print("One or more problems occurred during the initialization of the PFBExporter class")
        exit()

    pfb_export.initialize()
    pfb_export.export()
    pfb_export.filter_attributes(is_black_list=False)
    # pfb_export.filter_attributes(is_black_list=True)
    pfb_export.setup_and_run_analysis(analysis_script_consortia) #TODO how to find consortium
    pfb_export.to_ontology_code()
    pfb_export.add_external_references_material()
    pfb_export.zip()
    pfb_export.clean_up()
    print(pfb_export.config_source)


if __name__ == "__main__":
    main()

