import os
import mimetypes
import argparse
import mimetypes

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--path_to_file", type=str,
                    # default="output.txt",
                    required=True,
                    help="this is path to directory whith you want scan")
parser.add_argument("-d", "--path_to_catologue", type=str,
                    # default="/Users/Xrono/Desktop/python/new",
                    required=True,
                    help="this is path to the output file")
args = parser.parse_args()

PATH_TO_INPUT_CATOLOGUE = args.path_to_catologue
PATH_TO_OUTPUT_FILE = args.path_to_file

# PATH_TO_INPUT_CATOLOGUE = "/Users/Xrono/Desktop/python/new"
# PATH_TO_OUTPUT_FILE = "output.txt"


def write_information_to_output_file(file_from, file_to):

    with open(file_from) as file_open_temp:
        content = file_open_temp.readlines()
    with open(file_to, 'a') as file_out_temp:
        file_out_temp.write("".join(content))
        file_out_temp.write("".join('\n'))


def walk_through_tree_of_catalogue(in_cotalogue, out_file):
    if os.path.exists(in_cotalogue):
        if ((os.path.isfile(out_file) == True) or (
                os.path.exists(
                    str(os.path.split(
                        os.path.abspath(out_file))[0]) + '/') == True)):
            file_clean = open(out_file, 'w')
            file_clean.close()
            for d, dirs, files in os.walk(PATH_TO_INPUT_CATOLOGUE):
                # print "path: {0}\ndirectories {1}\nfiles {2}".format(d, dirs,
                # files)
                for f in files:
                    if str(os.path.splitext(f)[1]) != '':
                        if os.path.isfile(out_file):
                            write_information_to_output_file(
                                os.path.join(d, f), out_file)
        else:
            print "Wrong path to the file"
    else:
        print "No such directory"


walk_through_tree_of_catalogue(PATH_TO_INPUT_CATOLOGUE, PATH_TO_OUTPUT_FILE)
