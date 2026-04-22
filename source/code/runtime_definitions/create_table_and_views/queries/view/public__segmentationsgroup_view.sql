SET search_path TO "public", public;
DROP VIEW IF EXISTS "public"."segmentationsgroup_view";
CREATE OR REPLACE VIEW "public"."segmentationsgroup_view" AS
SELECT id,
    name,
    description
   FROM segmentationsgroups;
RESET search_path;
