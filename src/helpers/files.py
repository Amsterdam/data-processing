import os
import errno
import json
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


def save_file(data, output_folder, filename, suffix):
    """
        Save data to different file types, using folder, filename and suffix. 
        It currently works only with: (geo)json using .geojson or .json as suffix input
    """
    create_dir_if_not_exists(output_folder)
    full_path = os.path.join(output_folder, filename + suffix)
    if suffix in ('.geojson', 'json'):
        with open(full_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
    print("File saved here: {}".format(full_path))


def unzip(path, filename_as_folder=False):
    """
    Find all .zip files and unzip in root.
    Use filename_as_folder=True to unzip to subfolders with name of zipfile."""
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
                            raise  # re-raise exception if a different error occured

