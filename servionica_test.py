import os
import mimetypes
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--path_to_file", type=str, help="catologue")
parser.add_argument("-d", "--path_to_catologue", type=str, help="output file")
args = parser.parse_args()

PATH_TO_INPUT_CATOLOGUE = args.path_to_catologue
PATH_TO_OUTPUT_FILE = args.path_to_file


def write_information_to_output_file(file_from, file_to):
    with open(file_from) as file_open_temp:
        content = file_open_temp.readlines()
    with open(file_to, 'a') as file_out_temp:
        file_out_temp.write("".join(content))


def walk_through_tree_of_catalogue(in_cotalogue, out_file):
    for d, dirs, files in os.walk(PATH_TO_INPUT_CATOLOGUE):
        for f in files:
            print os.path.join(d, f)
            write_information_to_output_file(os.path.join(d, f), out_file)

walk_through_tree_of_catalogue(PATH_TO_INPUT_CATOLOGUE, PATH_TO_OUTPUT_FILE)
