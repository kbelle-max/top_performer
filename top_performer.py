"""
***************************************************************
An Example YAML parser that outputs Data as a CSV
***************************************************************
"""
import csv
import yaml
import xml.etree.ElementTree as ET
import json
import zipfile


def top_key_fns(string, _dict, path='/', path_list=[], top_subkey_list=[]):
    """
    returns a 2d list Where list 1 contains the path to the node containing 
    the string and list 2 contains  key with the highest value within that dictionary object.
    """
    for key, value in _dict.items():
        if string in key:
            top_subkey = ''
            top_score = 0
            for subkey, score in value.items():
                if score > top_score:
                    top_score = score
                    top_subkey = subkey
            path_list.append(path+key), top_subkey_list.append(top_subkey)
        else:
            top_key_fns(string, value, path=path+key+'/')
    return [path_list, top_subkey_list]


def main(string, inputdata='',parse_func=top_key_fns, outputfile='output.csv',data_type=''):
    """

    Parses YAML file searching for keys with the given string .
    Assumes that Key contains a dictionary and returns the subkey with the highest INT value
    Args:
    ------
    inputdata : Path to the YAML file containing  assignment data
    outputdir : Path to the output CSV containing  subkey with the highest integer value
    parse_func : Recursive function to ddetermine how to deal with each node.

    Returns:
    --------
    CSV highest integer value in that dictionary
    """
    yaml_file = inputdata.split('/')[-1]
    output_headers = ['inputstring_path', 'top_subkey']
    with open(inputdata, 'r') as stream:
        load_asignment = yaml.load(stream, Loader=yaml.FullLoader)
    node = parse_func(string, load_asignment, path=yaml_file+'/')
    with open(outputfile, 'w') as file_output:
        file = csv.writer(file_output)
        file.writerow(output_headers)
        for inputstring_path, top_subkey in zip(node[0], node[1]):
            file.writerow([inputstring_path, top_subkey])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--string', help='Input String')
    parser.add_argument('-i', '--inputdata',
                        help='Input YAML File')
    parser.add_argument('-o', '--outputdir',
                        default='output.csv', help='Output CSV')
    args = parser.parse_args()

    main(args.string, inputdata=args.inputdata,parse_func=top_key_fns, outputfile=args.outputdir)
