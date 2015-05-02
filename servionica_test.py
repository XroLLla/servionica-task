import os
from collections import OrderedDict
import argparse
import struct
import json

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
    # check path to cotalogue
    if os.path.exists(in_cotalogue):
        # check path to out_file
        if os.path.exists(str(os.path.split(
                os.path.abspath(out_file))[0]) + '/'):
            list_of_dict = []
            for d, dirs, files in os.walk(PATH_TO_INPUT_CATOLOGUE):
                for f in files:
                    with open(os.path.join(d, f), "rb") as binary_file:
                        # check qcow2 file
                        byte = binary_file.read(3)
                        if byte == "QFI":
                            fileqcow = os.path.join(d, f)
                            list_of_dict.append(get_qcow_file_dict(fileqcow))
        else:
            print "Wrong path to the file"
    else:
        print "No such directory"
    write_information_to_output_file(out_file, list_of_dict)


def snapshots_info(b_fileqcow, snap_offset):

    offset = get_info(b_fileqcow, snap_offset, 8, '>Q')
    len_id = get_info(b_fileqcow, snap_offset + 12, 2, '>H')
    len_name = get_info(b_fileqcow, snap_offset + 14, 2, '>H')
    snapshots_size = get_info(b_fileqcow, snap_offset + 32, 4, '>I')
    extra_data_size = get_info(b_fileqcow, snap_offset + 36, 4, '>I')
    snapshots_id = get_info(
                            b_fileqcow,
                            snap_offset + 40 + extra_data_size,
                            len_id, str(len_id) + 's'
                            )
    snapshots_name = get_info(
                                b_fileqcow,
                                snap_offset + 40 + extra_data_size + len_id,
                                len_name, str(len_name) + 's'
                                )
    len_of_ss = snap_offset + 40 + extra_data_size + len_id + len_name
    # check if offset not multiply 8 and plus missing bits
    if len_of_ss % 8 != 0:
        len_of_ss = len_of_ss + (8 - (len_of_ss % 8))
    # dictionary, which stores the input order of arguments
    snap_dict = OrderedDict()
    snap_dict['id'] = snapshots_id
    snap_dict['name'] = snapshots_name
    snap_dict['virtualsize'] = snapshots_size
    return (snap_dict, len_of_ss)


def get_qcow_file_dict(qcowfile):
    # dictionary, which stores the input order of arguments
    file_dictionary = OrderedDict()
    file_dictionary['filename'] = qcowfile
    size = os.path.getsize(qcowfile)
    file_dictionary['size'] = size
    with open(qcowfile, "rb") as binary_file:
        virtual_size = get_info(binary_file, 24, 8, '>Q')
        file_dictionary['virtualsize'] = virtual_size
        # check availability of backing file
        is_bf = check_bf_exist(binary_file)
        if is_bf:
            backing_file_name = get_bf_name(binary_file, is_bf)
            file_dictionary['backing_file'] = backing_file_name
        # check availability of snapshots
        is_snapshots = check_snapshots_exist(binary_file)
        if is_snapshots:
            file_dictionary['snapshots'] = []
            count_of_snapshots = is_snapshots
            snap_offset = get_info(
                binary_file, 64, 8, '>Q')
            # pass on all snapshots
            while count_of_snapshots > 0:
                snapshot_dict, snap_offset = snapshots_info(
                                            binary_file, snap_offset)
                file_dictionary['snapshots'].append(snapshot_dict)
                count_of_snapshots -= 1
    return file_dictionary


def write_information_to_output_file(file_to, dictionary):
    # write information about qcow2 file
    with open(file_to, 'w') as file_out_temp:
        json.dump(dictionary, file_out_temp, indent=2, ensure_ascii=False)


walk_through_tree_of_catalogue_qcow2(
    PATH_TO_INPUT_CATOLOGUE, PATH_TO_OUTPUT_FILE)
