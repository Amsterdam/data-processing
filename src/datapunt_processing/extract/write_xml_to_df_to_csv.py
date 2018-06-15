import xml.etree.ElementTree as ET
import pandas as pd
import argparse


class XML2DataFrame:
    """Class for parsing and XML to a Dataframe"""

    def __init__(self, xml_data):
        self.root = ET.parse(xml_data).getroot()[0]  # Get first emelent in XML

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def normalize(self, name):
        """
        Remove the schemaname from keys/values.
        input:
            {https://www.tenderned.nl/schema/tenderned-export}percelen
        returns:
            percelen
        """
        if name[0] == "{":
            uri, tag = name[1:].split("}")
            return tag
        else:
            return name

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[self.normalize(element.tag)] = self.normalize(element.text)
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)


def xml_to_df(file):
    """
    Function to parse an XML file to a Pandas dataframe.
    Args:
       file = filename of the XML
    Result:
        df of the xml
    """
    xml2df = XML2DataFrame(file)
    xml_dataframe = xml2df.process_data()
    return xml_dataframe


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Converts an XML file to CSV, using the first element in the root as a list of elements.

    Example command line:
        ``python write_xml_to_df_to_csv.py Aanbestedingen_2017-01-01_tot_2018-05-02.xml data``
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
    df = xml_to_df(args.full_path)
    file = args.full_path.split('/')[-1]
    file_name = file.split('.')[0]
    print('found the following keys: ', df.keys())
    df.to_csv(file_name+'.csv', sep=';')
    print('written file to {}/{}.csv'.format(args.output_folder, file_name))


if __name__ == '__main__':
    main()
