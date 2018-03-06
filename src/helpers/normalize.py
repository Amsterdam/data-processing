# -----------------
# Dict/Json stuff
# -----------------


def flatten_json(json_object):
    """
    Flatten nested json Object.

    Args:
        1 json_object, for example: {"key": "subkey": { "subsubkey":"value" }}

    Result:
        {"key.subkey.subsubkey":"value"}

    Source:
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

    flatten(json_object)
    return out


def clean_dict(dictionary, key_name):
    """
    Remove a field from a dict based on key name.

    Args:
        1. dictionary: {id:1, dates:2018-12-02}
        2. key_name: 'dates'

    Result:
        {id:1}
    """
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((clean_dict(dictionary), v) for k, v in dictionary.items() if k is not key_name)
