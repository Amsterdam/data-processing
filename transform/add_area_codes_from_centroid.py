#!/usr/bin/env python3
"""
This is where SQL queries that must be run after import go.
"""
import psycopg2
import configparser
import argparse

config = configparser.RawConfigParser()
config.read('auth.conf')

createGeom = """
ALTER TABLE crowscores
  DROP COLUMN IF EXISTS id;
ALTER TABLE crowscores 
  ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE crowscores
  DROP COLUMN IF EXISTS geom;
ALTER TABLE crowscores
  ADD COLUMN geom geometry;
UPDATE crowscores
    SET geom = 
      CASE 
        WHEN 
          maxx is not null
        THEN ST_SetSRID(ST_ENVELOPE(('LINESTRING('||minx::double precision||' '||miny::double precision||', '||maxx::double precision||' '||maxy::double precision||')')::geometry), 28992) 
        WHEN 
          "XMAX" is not null
        THEN ST_SetSRID(ST_ENVELOPE(('LINESTRING('||"XMIN"::double precision||' '||"YMIN"::double precision||', '||"XMAX"::double precision||' '||"YMAX"::double precision||')')::geometry), 28992) 
        WHEN 
          lon is not null
        THEN 
          ST_TRANSFORM(ST_PointFromText('POINT('||"lon"::double precision||' '||"lat"::double precision||')',4326),28992)
        WHEN 
          "RD-X" is not null and lat is null
        THEN 
          ST_PointFromText('POINT('||"RD-X"::double precision||' '||"RD-Y"::double precision||')',28992)
           ELSE null END;

CREATE INDEX geom_crowscores ON crowscores USING GIST(geom);

UPDATE crowscores
       SET (lat,lon) = (ST_Y(ST_TRANSFORM(ST_CENTROID(geom), 4326)), ST_X(ST_TRANSFORM(ST_CENTROID(geom), 4326)))
      WHERE lat is null or lat > 100
"""

addAreaCodes = """
DROP view if exists crowscores_csv CASCADE;
DROP TABLE IF EXISTS crowscores_totaal CASCADE;
SELECT 
  e.*, 
  g.naam as gebiedsnaam, 
  g.code as gebiedscode
INTO 
  crowscores_totaal
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
    (select * from crowscores) as c, 
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
ALTER TABLE crowscores_totaal 
ADD PRIMARY KEY (id);
"""

crowscoresView = """
DROP view if exists crowscores_csv CASCADE;
create view
  crowscores_csv
as select
  "Schouwronde", 
  "Volgnummer inspectie", 
  "Volgnummer score", 
  "Aanmaakdatum score"::timestamp as "Aanmaakdatum score", 
  "Inspecteur", 
  "Bestekspost", 
  "Score", 
  buurtcode, 
  buurtnaam,
  verblijfin, 
  wijkcode, 
  wijknaam
  stadsdeelcode,
  gebiedscode,
  gebiedsnaam, 
  stadsdeelnaam, 
  lon,lat
from
  crowscores_totaal
"""

def execute_sql(pg_str, sql):
    with psycopg2.connect(pg_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)


def get_pg_str(host, port, user, dbname, password):
    return 'host={} port={} user={} dbname={} password={}'.format(
        host, port, user, dbname, password
    )


def executeScriptsFromFile(pg_str, filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        print(command)
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            execute_sql(pg_str, command)
        except psycopg2.OperationalError as msg:
            print("Command skipped: {}".format(msg))


def main(dbConfig):
    print('Additional SQL run after import concludes.')
    pg_str = get_pg_str(config.get(dbConfig,'host'),config.get(dbConfig,'port'),config.get(dbConfig,'dbname'), config.get(dbConfig,'user'), config.get(dbConfig,'password'))
    execute_sql(pg_str, createGeom)
    print('geometry field created')
    execute_sql(pg_str, addAreaCodes)
    print('areaCode fields added')
    execute_sql(pg_str, crowscoresView)
    print('csv view Created')

if __name__ == '__main__':
    desc = "Run additional SQL."
    parser = argparse.ArgumentParser(desc)
    parser.add_argument('dbConfig', type=str,
                        help='dev or docker', nargs=1)
    args = parser.parse_args()
    main(args.dbConfig[0])