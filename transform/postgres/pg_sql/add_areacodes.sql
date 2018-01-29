DROP TABLE IF EXISTS crowscores_totaal;
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

