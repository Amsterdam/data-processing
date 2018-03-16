######################################################################
# Dict/Json stuff --> helper functions to manipulate json and dictionary objects
######################################################################

# to do: make some functions more generic

def flatten_json(json_object):
    """
    Flatten nested json Object.
    Args:
        1 json_object, for example: {"key": "subkey": { "subsubkey":"value" }}
    Returns:
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


def jsonPoints2geojson(df, latColumn, lonColumn):
    """
       Convert JSON with lat/lon columns to geojson.
       https://gis.stackexchange.com/questions/220997/pandas-to-geojson-multiples-points-features-with-python
    """
    geojson = {'type': 'FeatureCollection', 'features': []}
    for item in df:
        # logger.info(item)
        item = flatten_json(item)
        # logger.info(item.keys())
        keep_items = {}
        for k,v in item.items():
            if k in ['id', 'id_number', 'serial_number', 'well','location.address.summary', 'location.address.district', 'location.address.neighbourhood', 'owner.name', 'created_at', 'placing_date', 'operational_date', 'warranty_date','containers.0']:
                keep_items[k] = v
        # logger.info(keep_items)
        if lonColumn:
            feature = {'type': 'Feature',
                       'properties': keep_items}
            feature['geometry'] = {'type': 'Point',
                                   'coordinates': [float(item[lonColumn]),
                                                   float(item[latColumn])
                                                   ]}
            geojson['features'].append(feature)
    return geojson


def openJsonArrayKeyDict2FlattenedJson(fileName):
    """
        Open json and return array of objects without object value name.
        For example: [{'container':{...}}, {'container':{...}}] returns now as [{...},{...}])
    """
    with open(fileName, 'r') as response:
        data = json.loads(response.read())
        objectKeyName = list(data[0].keys())[0]
        # objectKeyName = str(objectKeyName, 'utf-8')
        logger.info(fileName + " object opened")
        data = [item[objectKeyName] for item in data]
        # logger.info(data[0])
    return data


def joinByKeyNames(geojson, dataset, key1, key2):
    """
    Insert data from dataset to geojson where key1 from dataset matches key2 from geojson
    """
    n = 1
    for feature in geojson['features']:
        #logger.info(feature["properties"])
        matches = [item for item in dataset
                   if item[key1] == feature["properties"].get(key2)]
        if matches:
            if 'owner' in (matches[0].keys()):
                del matches[0]['owner']
            feature['properties'].update(matches[0])
        else:
            feature['properties']['container'] = None
        n += 1
        #logger.info("{} of {}".format(n, len(geojson['features'])))
    return geojson


def clean_dict(dictionary, key_name):
    """
    Remove a field from a dict based on key name.
    Args:
        1. dictionary: {id:1, dates:2018-12-02}
        2. key_name: 'dates'
    Returns:
        {id:1}
    """
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((clean_dict(dictionary), v) for k, v in dictionary.items() if k is not key_name)