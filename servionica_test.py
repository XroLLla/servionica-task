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


def get_qcow_file_dict(qcowfile):
    file_dictionary = {}
    file_name = qcowfile
    file_dictionary['filename'] = file_name
    size = os.path.getsize(qcowfile)
    file_dictionary['size'] = size
    with open(qcowfile, "rb") as binary_file:
        virtual_size = get_info(binary_file, 24, 8, '>Q')
        file_dictionary['virtualsize'] = virtual_size
        is_bf = check_bf_exist(binary_file)
        if is_bf:
            backing_file_name = get_bf_name(binary_file, is_bf)
            file_dictionary['backing_file'] = backing_file_name
        is_snapshots = check_snapshots_exist(binary_file)
        if is_snapshots:
            file_dictionary['snapshots'] = []
            count_of_snapshots = is_snapshots
            snapshots_offset = get_info(
                binary_file, 64, 8, '>Q')
            while count_of_snapshots > 0:
                snapshot_dict, snapshots_offset = snapshots_info(binary_file, snapshots_offset)
                file_dictionary['snapshots'].append(snapshot_dict)
                count_of_snapshots -= 1
    return file_dictionary


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
                    with open(os.path.join(d, f), "rb") as binary_file:
                        byte = binary_file.read(3)
                        if byte == "QFI":
                            fileqcow = os.path.join(d, f)
                            qcow_file_dict = get_qcow_file_dict(fileqcow)
                            print (qcow_file_dict)
        else:
            print "Wrong path to the file"
    else:
        print "No such directory"


def snapshots_info(b_fileqcow, snapshots_offset):

    offset = get_info(b_fileqcow, snapshots_offset, 8, '>Q')
    len_id = get_info(b_fileqcow, snapshots_offset + 12, 2, '>H')
    len_name = get_info(b_fileqcow, snapshots_offset + 14, 2, '>H')
    snapshots_size = get_info(b_fileqcow, snapshots_offset + 32, 4, '>I')
    extra_data_size = get_info(b_fileqcow, snapshots_offset + 36, 4, '>I')
    snapshots_id = get_info(
                            b_fileqcow,
                            snapshots_offset + 40 + extra_data_size,
                            len_id, str(len_id) + 's'
                            )
    snapshots_name = get_info(
                                b_fileqcow,
                                snapshots_offset + 40 + extra_data_size + len_id,
                                len_name, str(len_name) + 's'
                                )
    len_of_ss = snapshots_offset + 40 + extra_data_size + len_id + len_name
    if len_of_ss % 8 != 0:
        len_of_ss = len_of_ss + (8 - (len_of_ss % 8))
    snap_dict = {
                 'id': snapshots_id,
                 'name': snapshots_name,
                 'virtual_size': snapshots_size
                }
    return (snap_dict, len_of_ss)


def write_information_to_output_file(file_to):

    with open(file_from) as file_open_temp:
        content = file_open_temp.readlines()
    with open(file_to, 'a') as file_out_temp:
        file_out_temp.write("".join(content))
        file_out_temp.write("".join('\n'))
walk_through_tree_of_catalogue_qcow2(
    PATH_TO_INPUT_CATOLOGUE, PATH_TO_OUTPUT_FILE)
