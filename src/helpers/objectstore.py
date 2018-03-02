import os
import logging
from swiftclient import client

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


class Objectstore(object):
    RESP_LIMIT = 10000  # serverside limit of the response

    def __init__(self, settings):
        self.settings = settings
        self.conn = client.Connection(authurl=settings['AUTHURL'],
                                      user=settings['USER'],
                                      key=settings['PASSWORD'],
                                      tenant_name=settings['TENANT_NAME'],
                                      auth_version=settings['VERSION'],
                                      os_options={'tenant_id': settings['TENANT_ID'],
                                                  'region_name': settings['REGION_NAME'],
                                                  'endpoint_type': 'internalURL'
                                                  })

    #def get_objectstore_object(self, object_meta_data):
    #    return self.conn.get_object(object_meta_data['container'], object_meta_data['name'])[1]


    prefixes = ['aanvalsplan_schoon/crow']
                #,'aanvalsplan_schoon/mora']

    def get_full_container_list(self, conn, container, **kwargs):

        # Note: taken from the bag_services project
        limit = 10000
        kwargs['limit'] = limit
        page = []

        seed = []

        _, page = conn.get_container(container, **kwargs)
        seed.extend(page)

        while len(page) == limit:
            # keep getting pages..
            kwargs['marker'] = seed[-1]['name']
            _, page = conn.get_container(container, **kwargs)
            seed.extend(page)

        return seed


    def download_container(self, conn, container, prefix, datadir):
        target_dir = os.path.join(datadir, prefix)
        os.makedirs(target_dir)  # will error out if directory exists

        content = get_full_container_list(conn, container, prefix=prefix)
        #print(content)
        for obj in content:
            if obj['content_type']!='application/directory':
                target_filename = os.path.join(datadir, obj['name'])
                #target_filename = obj['name']
                with open(target_filename, 'wb') as new_file:
                    _, obj_content = self.conn.get_object(container['name'], obj['name'])
                    new_file.write(obj_content)
            logger.info('Written file '+obj['name'])


    def download_containers(self, datasets, prefixes, datadir):
        """
        Download the schoonmonitor datasets from object store.

        Simplifying assumptions:
        * layout on data store matches intended layout of local data directory
        * datasets do not contain nested directories
        * assumes we are running in a clean container (i.e. empty local data dir)
        * do not overwrite / delete old data
        """
        logger.info('Checking local data directory exists and is empty')
        if not os.path.exists(datadir):
            raise Exception('Local data directory does not exist.')
        prefixes = prefixes.split(',')
        # listing = os.listdir(datadir)

        logger.info('Establishing object store connection.')
        resp_headers, containers = self.conn.get_account()

        logger.info("Response headers: %s" % resp_headers)
        for container in containers:
            logger.info(container)
        logger.info('Downloading containers ...')
        #dirName ='crow'

        containers = conn.get_container(datasets)
         #                            prefix='aanvalsplan_schoon/'+ dirName,)
        print(containers)
        prefixes = prefixes.split(',')
        for c in containers:
            for prefix in prefixes:
                download_container(self.conn, c, prefix, datadir)

    def get_full_container_list(self, conn, container, **kwargs) -> list:
        """
        get all files stored in container (incl. sub-containers)
        Args:
            conn = connection with the Objectstore (using swiftclient Connection API)
            container == "path/in/Objectstore"
        returns
            generator object
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
            _, lastpage = self.conn.get_container(container, **kwargs)
            for object_info in lastpage:
                yield object_info

        raise StopIteration

    def get_objectstore_objects(self, container, path):
        return self._get_full_container_list(self.conn, container, [], prefix=path)

    def get_objectstore_object(self, path):
        return self.conn.get_object(container, path)[1]

    def _get_full_container_list(self, conn, container, seed, **kwargs):
        kwargs['limit'] = self.RESP_LIMIT
        if len(seed):
            if 'subdir' in seed[1]:
                kwargs['marker'] = seed[-1]['subdir']
            else:
                kwargs['marker'] = seed[-1]['name']

        _, page = conn.get_container(container, **kwargs)
        seed.extend(page)
        return seed if len(page) < self.RESP_LIMIT else \
               self._get_full_container_list(conn, container, seed, **kwargs)

    def get_csvs(self, csv_identifier):
        csvs = []
        for container in settings.CONTAINERS:
            for month in self._get_subdirs(container, ''):
                for day in self._get_subdirs(container, month):
                    for trajectory in self._get_subdirs(container, day):
                        csvs.extend(self._get_csv_type(container, trajectory, csv_identifier))
        return csvs

    def get_detection_csvs(self, day):
        csvs = []
        log.info('day: {}'.format(day))
        for trajectory in self.get_datapunt_subdirs(day):
                for panorama in self.get_datapunt_subdirs(trajectory):
                    csvs.extend(self._get_datapunt_csv_type(panorama, 'region'))
        return csvs

    def get_objectstore_subdirs(self, path):
        objects_from_store = self._get_full_container_list(self.conn,
                                                           settings.CONTAINER,
                                                           [],
                                                           delimiter='/',
                                                           prefix=path)
        return [store_object['subdir'] for store_object in objects_from_store
                if 'subdir' in store_object]

    def _get_csv_type(self, container, path, csv_identifier):
        csvs = self._get_full_container_list(self.panorama_conn,
                                             container,
                                             [],
                                             delimiter='/',
                                             prefix=path+csv_identifier)
        for csv_object in csvs:
            csv_object['container'] = container
        return csvs

    def _get_objectstore_csv_type(self, path, csv_identifier):
        csvs = self._get_full_container_list(self.datapunt_conn,
                                             settings.CONTAINER,
                                             [],
                                             delimiter='/',
                                             prefix=path+csv_identifier)
        return csvs

    def put_into_objectstore(self, object_name, object_content, content_type):
        self.conn.put_object(settings.CONTAINER,
                             object_name,
                             contents=object_content,
                             content_type=content_type)

    def get_containerroot_csvs(self, csv_identifier):
        csvs = []
        for container in settings.CONTAINERS:
            csvs.extend(self._get_csv_type(container, '', csv_identifier))
        return csvs
