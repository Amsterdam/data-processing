#!/usr/bin/env python3
import argparse

from datapunt_processing.helpers.connections import psycopg_connection_string, execute_sql
from datapunt_processing import logger

from datapunt_processing.load import load_wfs_to_postgres

logger = logger()

# SQL Queries

createDummyTable = """
DROP TABLE IF EXISTS test_areacodes CASCADE;
CREATE TABLE test_areacodes
  (name text, 
   lat double precision, 
   lon double precision,
   "X" double precision,
   "Y" double precision);
INSERT INTO test_areacodes VALUES
  ('Dam', 52.3731081,4.8932945),
  ('Sportpark Elzenhagen Noord', 52.3975308,4.9253285);
"""
createGeom = """
ALTER TABLE test_areacodes 
  ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE test_areacodes
  DROP COLUMN IF EXISTS geom;
ALTER TABLE test_areacodes
  ADD COLUMN geom geometry;
UPDATE test_areacodes
    SET geom = 
      CASE 
        WHEN 
          lon is not null
        THEN 
          ST_TRANSFORM(ST_PointFromText('POINT('||"lon"::double precision||' '||"lat"::double precision||')',4326),28992)
        WHEN 
          "X" is not null and lat is null
        THEN 
          ST_PointFromText('POINT('||"X"::double precision||' '||"Y"::double precision||')',28992)
           ELSE null END;

CREATE INDEX geom_test_areacodes ON test_areacodes USING GIST(geom);

UPDATE test_areacodes
       SET (lat,lon) = (ST_Y(ST_TRANSFORM(ST_CENTROID(geom), 4326)), ST_X(ST_TRANSFORM(ST_CENTROID(geom), 4326)))
      WHERE lat is null or lat > 100
"""

addAreaCodes = """
DROP view if exists test_areacodes_csv CASCADE;
DROP TABLE IF EXISTS test_areacodes_totaal CASCADE;
SELECT 
  e.*, 
  g.naam as gebiedsnaam, 
  g.code as gebiedscode
INTO 
  test_areacodes_totaal
FROM
   (SELECT 
     c.*, 
     d.stadsdeelcode,
     d.buurtcode,
     d.wijkcode,
     d.stadsdeelnaam,
     d.buurtnaam,
     d.wijknaam
  FROM 
    (select * from test_areacodes) as c, 
    (SELECT 
       a.stadsdeelcode,
       a.buurtcode,
       w.vollcode as wijkcode,
       a.stadsdeelnaam,
       a.buurtnaam,
       w.naam as wijknaam,
       a.wkb_geometry
     FROM
     (  SELECT 
        s.naam as stadsdeelnaam,
        s.code as stadsdeelcode,
        b.naam as buurtnaam,
        s.code || b.code as buurtcode,
        b.wkb_geometry
        FROM 
          buurt as b, 
          stadsdeel as s
        WHERE ST_WITHIN(ST_CENTROID(b.wkb_geometry),s.wkb_geometry)
      ) as a, 
      buurtcombinatie as w
    WHERE ST_WITHIN(ST_CENTROID(a.wkb_geometry),w.wkb_geometry)) as d
  WHERE ST_WITHIN(ST_CENTROID(c.geom), d.wkb_geometry)
  ) as e,
  gebiedsgerichtwerken as g
WHERE ST_WITHIN(ST_CENTROID(e.geom), g.wkb_geometry);
ALTER TABLE test_areacodes_totaal 
ADD PRIMARY KEY (id);
"""

test_areacodesView = """
DROP view if exists test_areacodes_csv CASCADE;
create view
  test_areacodes_csv
as select
  id,
  name,
  buurtcode, 
  buurtnaam,
  wijkcode, 
  wijknaam
  stadsdeelcode,
  gebiedscode,
  gebiedsnaam, 
  stadsdeelnaam, 
  lon,lat
from
  test_areacodes_totaal
"""


def executeScriptsFromFile(pg_str, filename):
    """WIP does not work yet"""
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        logger.info(command)
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            execute_sql(pg_str, command)
        except psycopg2.OperationalError as msg:
            logger.info("Command skipped: {}".format(msg))


def parser():
    description = """
    Loads WFS areas into Postgres and joins all the names and codes to a dummy table by using lat lon or X,Y.

    Use ENV for ogr2ogr if using this in a virtual env:
        ``export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH``

    Example command line:
        ``postgres_add_areas_from_coordinates config.ini dev``
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('full_config_path',
                        type=str,
                        help="""write the full config.ini path including the name. For example authentication/config.ini""")
    parser.add_argument('db_config_name',
                        type=str,
                        help='dev or docker')
    return parser


def main():
    args = parser().parse_args()
    pg_str = psycopg_connection_string(args.full_config_path, args.db_config_name)

    load_wfs_to_postgres.main()  # Reuses pg_str

    execute_sql(pg_str, createDummyTable)
    logger.info('created createDummyTable')
    execute_sql(pg_str, createGeom)
    logger.info('geometry field created')
    execute_sql(pg_str, addAreaCodes)
    logger.info('areaCode fields added')
    execute_sql(pg_str, test_areacodesView)
    logger.info('csv view Created')


if __name__ == '__main__':
    main()
