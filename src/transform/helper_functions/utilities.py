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
    remove a filed from a dict based in key name
    """
    if not isinstance(d, dict):
        return d
    return dict((cleandict(k), v) for k,v in d.items() if k is not 'dates')
