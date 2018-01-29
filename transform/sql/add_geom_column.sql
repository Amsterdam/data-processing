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
	      "X" is not null
	    THEN 
	      ST_PointFromText('POINT('||"X"::double precision||' '||"Y"::double precision||')',28992)
            WHEN 
              maxx is not null
             -- create polygon from minmax
           THEN ST_SetSRID(ST_ENVELOPE(('LINESTRING('||minx||' '||miny||', '||maxx||' '||maxy||')')::geometry), 28992) 
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