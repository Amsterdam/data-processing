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
        Create directory if it does not yet exists. directory can be set as: `dir/anotherdir`
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def save_file(data, output_folder, filename):
    """
        Save data to different file types, using folder, filename and suffix.
        It reads the filename suffix and saves the file as the appropriate type.
        save_file currently works with: csv, txt, geojson and json as suffixes.
        for example filename = data_output.csv or data_output.json
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
        Find all .zip files and unzip in root.
        Use filename_as_folder=True to unzip to subfolders with name of zipfile.
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
