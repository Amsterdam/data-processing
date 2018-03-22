import os
import errno
import json
import csv
from zipfile import BadZipfile, ZipFile


# -----------------
#: File System stuff
# -----------------
def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.

    Args:
        Specify the name of directory, for example: `dir/anotherdir`

    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def save_file(data, output_folder, filename):
    """
        save_file currently works with: csv, txt, geojson and json as suffixes.
        It reads the filename suffix and saves the file as the appropriate type.

        Args:
            1. data: list of flattened dictionary objects for example: [{id:1, attr:value, attr2:value}, {id:2, attr:value, attr2:value}]
            2. filename: data_output.csv or data_output.json
            3. output_folder: dir/anotherdir

        Returns:
            Saved the list of objects to the given geojson or csv type.
    """
    create_dir_if_not_exists(output_folder)
    suffix = filename.split('.')[-1]
    full_path = os.path.join(output_folder, filename)
    if suffix in ('geojson', 'json'):
        with open(full_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
    if suffix in ('csv', 'txt'):
        with open(full_path, 'w') as out_file:
            # get header titles based on first object in array
            header = list(data[0].keys())
            csvWriter = csv.writer(out_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(header)
            for row in data:
                csvWriter.writerow(row.values())

    print("File saved here: {}".format(full_path))


def unzip(path, filename_as_folder=False):
    """
    Find all zip files and unzip in root.

    Args:
        1. path: set the folder to check for zip files.
        2. filename_as_folder:Set it to True to unzip to subfolders with name of zipfile instead of in the root folder.

    Returns:
        Unzipped files in the path directory or in the path/name of the zip file.
    """
    for filename in os.listdir(path):
        if filename.endswith(".zip"):
            name = os.path.splitext(os.path.basename(filename))[0]
            if not os.path.isdir(name):
                try:
                    file = os.path.join(path, filename)
                    zip = ZipFile(file)
                    if filename_as_folder:
                        directory = os.path.join(path, name)
                        os.mkdir(directory)
                        print("Unzipping {} to {}".format(filename, directory))
                        zip.extractall(directory)
                    else:
                        print("Unzipping {} to {}".format(filename, path))
                        zip.extractall(path)
                except BadZipfile:
                    print("BAD ZIP: " + filename)
                    try:
                        os.remove(file)
                    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
                        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                            raise  # re-raise exception if a different error occured.
