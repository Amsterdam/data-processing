# data-processing
Data preparation scripts for analysis projects.

This repo is a WIP so the scripts do not work properly yet.

## Structure
The basic template uses these 4 types of scripts

### Auth
Fill in the config.ini.example with the proper user credentials for the project and rename this file to config.ini.
Do not store passwords in this file and use .gitignore to ignore .ini files to prevent uploading them to github.

 * Login to objectstore
 * Login to dev/docker databases
 * Access token to retrieve authen ticated data from data.amsterdam.nl api's.
    
### Extract
* Load files from the objectstore
* Load files from the data.amsterdam.nl catalog
* Load files through scraping a website

### Transform
* Cleaning
        - Get BAG adress
* Merging files with Pandas
* Geo enrichment
        - X, Y columns to WKT
* Add area codes to geo points
        - Postgres
        - Pandas

    
### Load
  * Load XLS to Postgres
  * Load JSON to Postgres
  * Save output to CSV
  * Save output to Geojson


