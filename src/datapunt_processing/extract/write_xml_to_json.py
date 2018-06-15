import os
import xmltodict
import json
import argparse


def xml2json(file_input, output_name):
    """Args:
       - full path name
       - full output file name
    """
    with open(file_input, 'rb') as data:
        with open(output_name, 'w') as outfile:
            json.dump(xmltodict.parse(data), outfile)


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Converts an XML file to JSON, keeping the nested structure.

    Example command line:
        ``python write_xml_to_json.py Aanbestedingen_2017-01-01_tot_2018-05-02.xml data``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('full_path',
                        type=str,
                        help='Add full filename and path to XML, for example data/myXML.xml')
    parser.add_argument('output_folder',
                        type=str,
                        help='Specify the desired output folder path, for example: app/data')
    return parser


def main():
    args = parser().parse_args()
    file = args.full_path.split('/')[-1]
    file_name = file.split('.')[0]
    suffix = '.json'
    xml2json(args.full_path, os.path.join(args.output_folder,file_name)+suffix)
    #print('found the following keys: ', df.keys())
    #df.to_csv(file_name+'.csv', sep=';')
    print('written file to {}/{}.json'.format(args.output_folder, file_name))


if __name__ == '__main__':
    main()