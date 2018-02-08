###############################################################################
# functions to dowload data from the Cloud VPS Objectstore
###############################################################################

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
config = configparser.RawConfigParser()
config.read('auth.conf')

# get config from auth.conf 
OBJECTSTORE = dict(
    VERSION = config.get('objectstore', 'VERSION'),
    AUTHURL = config.get('objectstore', 'AUTHURL'),
    TENANT_NAME = config.get('objectstore', 'TENANT_NAME'),
    TENANT_ID = config.get('objectstore', 'TENANT_ID'),
    USER = config.get('objectstore', 'USER'),
    PASSWORD = config.get('objectstore', 'PASSWORD'),
    REGION_NAME = config.get('objectstore', 'REGION_NAME')
)



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


def get_object(connection, object_meta_data: dict, dirname: str):
    """
    Download object from objectstore.
    object_meta_data is an object returned when using 'get_full_container_list'
    """
    return connection.get_object(dirname, object_meta_data['name'])[1]

def download_files(file_list):
    """Download the latest data. """
    for _, source_data_file in file_list:
        sql_gz_name = source_data_file['name'].split('/')[-1]
        msg = 'Downloading: %s' % (sql_gz_name)
        log.debug(msg)

        new_data = get_object(
            mora_conn, source_data_file, 'Dataservices')

        # save output to file!
        with open('data/{}'.format(sql_gz_name), 'wb') as outputzip:
            outputzip.write(new_data)
            

def get_full_container_list(conn, container, **kwargs) -> list:
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
    
def get_latest_mora_files():
    """
    Download the expected files provided by mks / kpn
    """
    file_list = []

    meta_data = get_full_container_list(
        mora_conn, 'Dataservices')

    for o_info in meta_data:
        for expected_file in EXPECTED_FILES:
            if not o_info['name'].endswith(expected_file):
                continue

            dt = parser.parse(o_info['last_modified'])
            now = datetime.datetime.now()

            delta = now - dt

            log.debug('AGE: %d %s', delta.days, expected_file)


            log.debug('%s %s', EXPECTED_FILES, dt)
            file_list.append((dt, o_info))

    download_files(file_list)

    
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