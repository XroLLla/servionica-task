
import os
import parse_arg
import qcow_file_info as qcow
import file_operation as file_o


def main(in_cotalogue, out_file):
    # check path to cotalogue
    if os.path.exists(in_cotalogue):
        # check path to out_file
        if os.path.exists(str(os.path.split(
                os.path.abspath(out_file))[0]) + '/'):
            list_of_dict = []
            for d, dirs, files in os.walk(parse_arg.PATH_TO_INPUT_CATOLOGUE):
                for f in files:
                    with open(os.path.join(d, f), "rb") as binary_file:
                        # check qcow2 file
                        byte = binary_file.read(3)
                        if byte == "QFI":
                            fileqcow = os.path.join(d, f)
                            list_of_dict.append(qcow.get_qcow_file_dict(fileqcow))
        else:
            print "Wrong path to the file"
    else:
        print "No such directory"
    file_o.write_information_to_output_file(out_file, list_of_dict)

if __name__ == '__main__':
    main(parse_arg.PATH_TO_INPUT_CATOLOGUE, parse_arg.PATH_TO_OUTPUT_FILE)
