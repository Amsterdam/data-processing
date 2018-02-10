import os
import errno
import json

# -----------------
# Dict/Json stuff
# -----------------
def flatten_json(jsonObject):
    """
        Flatten nested json Object {"key": "subkey": { "subsubkey":"value" }} to ['key.subkey.subsubkey'] values
        https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(jsonObject)
    return out


def clean_dict(d):
    """
        Remove a field from a dict based on key name.
    """
    if not isinstance(d, dict):
        return d
    return dict((cleandict(k), v) for k,v in d.items() if k is not 'dates')


# -----------------
# File System stuff
# -----------------
def create_dir_if_not_exists(directory):
    """
        Create directory if it does not yet exists. directory can be set as: 'dir/anotherdir' (in quotes).
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
    if suffix in ('.geojson','json'):
        with open(full_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
    print("File saved here: {}".format(full_path))
