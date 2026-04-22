SET search_path TO "interview", public;
DROP VIEW IF EXISTS "interview"."site_master_view";
CREATE OR REPLACE VIEW "interview"."site_master_view" AS
SELECT site_number,
    site_name,
    site_city,
    site_postal_code,
    site_region,
    site_brand,
    site_format
   FROM interview.site_master;
RESET search_path;
