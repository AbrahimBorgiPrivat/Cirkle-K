SET search_path TO "public", public;
DROP VIEW IF EXISTS "public"."loyality_customers_view";
CREATE OR REPLACE VIEW "public"."loyality_customers_view" AS
WITH dar_adresse AS (
         SELECT hn.id,
            split_part(hn.adgangsadressebetegnelse, ','::text, 1) AS adresse,
            pn.postnr::bigint AS postnr,
            st_x(st_transform(st_setsrid(st_geomfromtext(apunkt.pos), 32632), 4326)) AS longitude,
            st_y(st_transform(st_setsrid(st_geomfromtext(apunkt.pos), 32632), 4326)) AS latitude
           FROM datafordeler.dar_husnummer hn
             JOIN datafordeler.dar_adressepunkt apunkt ON apunkt.id = hn.adgangspunkt_id
             JOIN datafordeler.dar_postnummer pn ON pn.id = hn.postnummer_id
          WHERE hn.status = '3'::text
        ), stations_geo AS (
         SELECT sta.pno,
            sta.address,
            sta.zipcode,
            sta.city,
                CASE
                    WHEN da.postnr >= 0 AND da.postnr <= 2999 THEN 'København'::text
                    WHEN da.postnr >= 3000 AND da.postnr <= 3699 THEN 'Sjælland'::text
                    WHEN da.postnr >= 3700 AND da.postnr <= 3999 THEN 'Bornholm'::text
                    WHEN da.postnr >= 4000 AND da.postnr <= 4999 THEN 'Sjælland'::text
                    WHEN da.postnr >= 5000 AND da.postnr <= 5999 THEN 'Fyn'::text
                    WHEN da.postnr >= 6000 AND da.postnr <= 7999 THEN 'Sydjylland'::text
                    WHEN da.postnr >= 8000 AND da.postnr <= 8999 THEN 'Midtjylland'::text
                    WHEN da.postnr >= 9000 AND da.postnr <= 9999 THEN 'Nordjylland'::text
                    ELSE 'Ukendt'::text
                END AS region,
            da.longitude,
            da.latitude
           FROM stations sta
             LEFT JOIN dar_adresse da ON da.postnr = sta.zipcode::bigint AND da.adresse ~~* split_part(sta.address, '-'::text, 1)
          WHERE sta.enddate IS NULL AND da.id IS NOT NULL
        )
 SELECT lc.loyalty_id,
    lc.name,
    lc.phone,
    lc.email,
    lc.country,
    lc.primary_station,
    lc.segmentationgroup,
    lc.signed_up,
    EXTRACT(year FROM lc.signed_up) AS signup_year,
    EXTRACT(month FROM lc.signed_up) AS signup_month,
    lc.signed_up::date AS signup_date,
    EXTRACT(hour FROM lc.signed_up) AS signup_hour,
    EXTRACT(minute FROM lc.signed_up) AS signup_minute,
    lc.perm_notify,
    lc.perm_email,
    lc.perm_sms,
    lc.perm_survey,
    sg.address,
    sg.zipcode,
    sg.city,
    sg.region,
    sg.longitude,
    sg.latitude
   FROM loyality_customers lc
     JOIN stations_geo sg ON sg.pno = lc.primary_station;
RESET search_path;
