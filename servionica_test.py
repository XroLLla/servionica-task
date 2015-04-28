import os
import mimetypes
import argparse
import struct

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


def get_info(b_fileqcow, start_position, cout_of_reading_bytes, unpack_format):
    b_fileqcow.seek(start_position, 0)
    return struct.unpack(
        unpack_format, b_fileqcow.read(cout_of_reading_bytes))[0]


def check_bf_exist(b_fileqcow):
    backing_file_offset = get_info(b_fileqcow, 8, 8, '>Q')
    if backing_file_offset:
        return backing_file_offset
    else:
        return None


def get_bf_name(b_fileqcow, backing_file_offset):
    backing_file_size = get_info(b_fileqcow, 16, 4, '>I')
    backing_file_name = get_info(
                                    b_fileqcow,
                                    backing_file_offset,
                                    backing_file_size,
                                    str(backing_file_size) + 's')
    return backing_file_name


def check_snapshots_exist(b_fileqcow):
    nb_snapshots = get_info(b_fileqcow, 60, 4, '>I')
    if nb_snapshots:
        return nb_snapshots
    else:
        return None


def walk_through_tree_of_catalogue_qcow2(in_cotalogue, out_file):
    if os.path.exists(in_cotalogue):
        if os.path.exists(str(os.path.split(
                os.path.abspath(out_file))[0]) + '/'):
            file_clean = open(out_file, 'w')
            file_clean.close()
            for d, dirs, files in os.walk(PATH_TO_INPUT_CATOLOGUE):
                for f in files:
                    if str(os.path.splitext(f)[1]) != '':
                        with open(os.path.join(d, f), "rb") as bf:
                            print "\n\nfile name : {}".format(f)
                            byte = bf.read(3)
                            if byte == "QFI":
                                size = os.path.getsize(os.path.join(d, f))
                                print "size of file = {}".format(size)
                                virtual_size = get_info(bf, 24, 8, '>Q')
                                print "virtual size = {}".format(virtual_size)
                                is_bf = check_bf_exist(bf)
                                if is_bf:
                                    backing_file_name = get_bf_name(bf, is_bf)
                                    print "backing file name = {}".format(
                                        backing_file_name)
                                else:
                                    print "No backing file"
                                is_snapshots = check_snapshots_exist(bf)
                                if is_snapshots:
                                    print "There are {} snapshots".format(
                                        is_snapshots)
                                    snapshots_offset = get_info(
                                        bf, 64, 8, '>Q')

                                else:
                                    print "there is no snapshots"
        else:
            print "Wrong path to the file"
    else:
        print "No such directory"


def snapshots_info()


def write_information_to_output_file(file_from, file_to):

    with open(file_from) as file_open_temp:
        content = file_open_temp.readlines()
    with open(file_to, 'a') as file_out_temp:
        file_out_temp.write("".join(content))
        file_out_temp.write("".join('\n'))
walk_through_tree_of_catalogue_qcow2(
    PATH_TO_INPUT_CATOLOGUE, PATH_TO_OUTPUT_FILE)
