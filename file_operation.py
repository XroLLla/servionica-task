import os
import json


def write_information_to_output_file(file_to, dictionary):
    # write information about qcow2 file
    with open(file_to, 'w') as file_out_temp:
        json.dump(dictionary, file_out_temp, indent=2, ensure_ascii=False)


def read_json(file_out):
    file_data = json.loads(open(file_out).read())
    print len(file_data)
    return file_data