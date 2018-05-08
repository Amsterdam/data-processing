#!/usr/bin/env python3
import psycopg2
from psycopg2 import sql
from datetime import datetime
import argparse
import os
from datapunt_processing.helpers.files import create_dir_if_not_exists
from datapunt_processing.helpers.connections import psycopg_connection_string


def write_table_to_geojson(config_path, db_config, table_name, output_folder):
    """
    Export table to a GeoJson file.

    Args:
      1. pg_str: psycopg2 connection string, for example:
         host=localhost port=5432 user=your_username dbname=your_database_name password=very_secret
      2. table_name: for example my_tablename
      3. output_folder: define output folder, for example: /app/data

    Result:
      Exported file to output_folder/table_name_2018-12-31.geojson
    """
    pg_str = psycopg_connection_string(config_path, db_config)
    with psycopg2.connect(pg_str) as conn:
        with conn.cursor() as cursor:
            query = sql.SQL("""
    COPY
    (SELECT jsonb_build_object(
        'type',     'FeatureCollection',
        'features', jsonb_agg(feature)
    )
    FROM (
      SELECT jsonb_build_object(
        'type',       'Feature',
        'id',         id,
        'geometry',   ST_AsGeoJSON(ST_TRANSFORM(geom,4326))::jsonb,
        'properties', to_jsonb(row) - 'id' - 'geom'
      ) AS feature
      FROM (SELECT * FROM {}) row) features)
    TO STDOUT""").format(sql.Identifier(table_name))
            filename = "{}_{}.json".format(table_name, datetime.now().date())
            create_dir_if_not_exists(output_folder)
            full_path = os.path.join(output_folder, filename)
            with open(full_path, "w") as file:
                cursor.copy_expert(query, file)
                return(full_path)


def parser():
    desc = """
    Export Postgres table to geojson file with export date.

    Command line example:

        ``python write_table_to_geojson.py config.ini dev table_name data``

    Result:

        'table_name_yyy-mm-dd.json'
    """
    parser = argparse.ArgumentParser(desc)
    parser.add_argument(
        'config_path',
        type=str,
        help='Add full filepath of config.ini file, for example auth/config.ini')
    parser.add_argument(
        'dbconfig', type=str,
        help='dev or docker')
    parser.add_argument(
        'table_name',
        type=str,
        help='Insert table name, for example my_tablename')
    parser.add_argument(
        'output_folder',
        type=str,
        help='Define output folder, for example: /app/data')
    return parser


def main():
    args = parser().parse_args()
    csv_location = export_table_to_csv(args.config_path, args.dbconfig, args.table_name, args.output_folder)
    print('Exported to: {}'.format(csv_location))


if __name__ == '__main__':
    main()
