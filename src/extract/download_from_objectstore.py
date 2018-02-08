"""
Access the druktemonitor project data on the data store.

For now the convention is that only relevant files are in the datastore and
the layout there matches the layout expected by our data loading scripts.

(We may have to complicate this in the future if we get to automatic
delivery of new data for this project.)
"""

import os
import argparse
import logging
import configparser

from swiftclient.client import Connection

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('swiftclient').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def readConfig(configfile):
    config = configparser.RawConfigParser()
    config.read(configfile)
    print(config.sections())
    return(config)


config = readConfig('config.ini')
#OBJECTSTORE_PASSWORD = os.environ['EXTERN_DATASERVICES_PASSWORD']
OBJECTSTORE_PASSWORD = config.get('objectstore', 'OS_PASSWORD')

OS_CONNECT = {
    'VERSION': config.get('objectstore','ST_AUTH_VERSION'),
    'AUTHURL': config.get('objectstore','OS_AUTH_URL'),
    'TENANT_NAME': config.get('objectstore','OS_TENANT_NAME'),
    'USER': config.get('objectstore','OS_USERNAME'),
    'os_options': {
        'TENANT_ID': config.get('objectstore','OS_PROJECT_ID'),  # Project ID
        'REGION_NAME': config.get('objectstore','OS_REGION_NAME')
    },
    'PASSWORD': OBJECTSTORE_PASSWORD
}


DATASETS = set([
    'Dataservices'
])

prefixes = ['aanvalsplan_schoon/mora']
            #,'aanvalsplan_schoon/mora']

    
def get_connection(store_settings: dict) -> Connection:
    """
    get an objectsctore connection
    """
    store = store_settings

    os_options = {
        'tenant_id': store['TENANT_ID'],
        'region_name': store['REGION_NAME'],
        # 'endpoint_type': 'internalURL'
    }

    # when we are running in cloudvps we should use internal urls
    use_internal = os.getenv('OBJECTSTORE_LOCAL', '')
    if use_internal:
        os_options['endpoint_type'] = 'internalURL'

    connection = Connection(
        authurl=store['AUTHURL'],
        user=store['USER'],
        key=store['PASSWORD'],
        tenant_name=store['TENANT_NAME'],
        auth_version=store['VERSION'],
        os_options=os_options
    )

    return connection

    
    
def get_full_container_list(conn, container, **kwargs) -> list:
    """ 
    List all available data sources in the specific data container specific to the os connection 
    Returns a generator object.
    """
    limit = 10000
    kwargs['limit'] = limit
    page = []

    _, page = conn.get_container(container, **kwargs)
    lastpage = page
    for object_info in lastpage:
        yield object_info

    while len(lastpage) == limit:
        # keep getting pages..
        kwargs['marker'] = lastpage['name']
        _, lastpage = conn.get_container(container, **kwargs)
        for object_info in lastpage:
            yield object_info

    raise StopIteration
    

def download_container(conn, container, prefix, datadir):
    
    #target_dir = os.path.join(datadir, prefix)
    #os.makedirs(target_dir)  # will error out if directory exists
    
    content = get_full_container_list(conn, container, prefix=prefix)
    print(content)
    for obj in content:
        if obj['content_type']!='application/directory':
            target_filename = os.path.join(datadir, obj['name'])
            #target_filename = obj['name']
            with open(target_filename, 'wb') as new_file:
                _, obj_content = conn.get_object(container, obj['name'])
                new_file.write(obj_content)
        logger.debug('Written file '+obj['name'])


def download_containers(conn, datasets, datadir):
    """
    Download the schoonmonitor datasets from object store.

    Simplifying assumptions:
    * layout on data store matches intended layout of local data directory
    * datasets do not contain nested directories
    * assumes we are running in a clean container (i.e. empty local data dir)
    * do not overwrite / delete old data
    """
    logger.debug('Checking local data directory exists and is empty')
    if not os.path.exists(datadir):
        raise Exception('Local data directory does not exist.')

    listing = os.listdir(datadir)
    if listing:
        if len(listing) == 1 and listing[0] == 'README':
            # Case where the 'data' dictory is used from a fresh checkout.
            pass
        else:
            raise Exception('Local data directory not empty!')

    #logger.debug('Establishing object store connection.')
    resp_headers, containers = conn.get_account()

    logger.debug('Downloading containers ...')
    #dirName ='crow'

    #containers = conn.get_container('Dataservices',
     #                            prefix='aanvalsplan_schoon/'+ dirName,)
    #print(containers)

    for c in containers:
        if c['name'] in datasets:
            for prefix in prefixes:
                download_container(conn, c, prefix, datadir)


def main(datadir):
    conn = Connection(**OS_CONNECT)
    download_containers(conn, DATASETS, datadir)


if __name__ == '__main__':
    desc = "Download data from objectore."
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('datadir', type=str,
                        help='Local data directory.', nargs=1)
    args = parser.parse_args()

    # Check whether local cached downloads should be used.
    ENV_VAR = 'EXTERNAL_DATASERVICES_USE_LOCAL'
    use_local = True if os.environ.get(ENV_VAR, '') == 'TRUE' else False

    if not use_local:
        main(args.datadir[0])
    else:
        logger.info('No download from datastore requested, quitting.')