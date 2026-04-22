SET search_path TO "interview", public;
DROP VIEW IF EXISTS "interview"."item_master_view";
CREATE OR REPLACE VIEW "interview"."item_master_view" AS
SELECT im.item_number,
    im.item_name,
    im.item_subcategory,
    ii.img_url
   FROM interview.item_master im
     LEFT JOIN interview.item_images ii ON ii.item_number = im.item_number;
RESET search_path;
