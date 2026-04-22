SET search_path TO "public", public;
DROP VIEW IF EXISTS "public"."stations_view";
CREATE OR REPLACE VIEW "public"."stations_view" AS
WITH dar_adresse AS (
         SELECT hn.id,
            hn.adgangsadressebetegnelse,
            hn.husnummertekst,
            split_part(hn.adgangsadressebetegnelse, ','::text, 1) AS adresse,
            pn.postnr::bigint AS postnr,
            apunkt.pos AS positionpoint,
            st_x(st_transform(st_setsrid(st_geomfromtext(apunkt.pos), 32632), 4326)) AS longitude,
            st_y(st_transform(st_setsrid(st_geomfromtext(apunkt.pos), 32632), 4326)) AS latitude
           FROM datafordeler.dar_husnummer hn
             JOIN datafordeler.dar_adressepunkt apunkt ON apunkt.id = hn.adgangspunkt_id
             JOIN datafordeler.dar_postnummer pn ON pn.id = hn.postnummer_id
          WHERE hn.status = '3'::text
        )
 SELECT sta.pno,
    sta.vat,
    sta.name,
    sta.address,
    sta.zipcode,
    sta.city,
    sta.startdate,
    sta.enddate,
        CASE
            WHEN dar_adresse.postnr >= 0 AND dar_adresse.postnr <= 2999 THEN 'København'::text
            WHEN dar_adresse.postnr >= 3000 AND dar_adresse.postnr <= 3699 THEN 'Sjælland'::text
            WHEN dar_adresse.postnr >= 3700 AND dar_adresse.postnr <= 3999 THEN 'Bornholm'::text
            WHEN dar_adresse.postnr >= 4000 AND dar_adresse.postnr <= 4999 THEN 'Sjælland'::text
            WHEN dar_adresse.postnr >= 5000 AND dar_adresse.postnr <= 5999 THEN 'Fyn'::text
            WHEN dar_adresse.postnr >= 6000 AND dar_adresse.postnr <= 7999 THEN 'Sydjylland'::text
            WHEN dar_adresse.postnr >= 8000 AND dar_adresse.postnr <= 8999 THEN 'Midtjylland'::text
            WHEN dar_adresse.postnr >= 9000 AND dar_adresse.postnr <= 9999 THEN 'Nordjylland'::text
            ELSE 'Ukendt'::text
        END AS region,
    dar_adresse.longitude,
    dar_adresse.latitude
   FROM stations sta
     LEFT JOIN dar_adresse ON dar_adresse.postnr = sta.zipcode::bigint AND dar_adresse.adresse ~~* split_part(sta.address, '-'::text, 1)
  WHERE sta.enddate IS NULL AND dar_adresse.id IS NOT NULL;
RESET search_path;
