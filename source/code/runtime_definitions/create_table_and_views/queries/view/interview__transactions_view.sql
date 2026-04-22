SET search_path TO "interview", public;
DROP VIEW IF EXISTS "interview"."transactions_view";
CREATE OR REPLACE VIEW "interview"."transactions_view" AS
SELECT id,
    site_number,
    trn_transaction_date,
    trn_promotion_id,
        CASE
            WHEN trn_promotion_id = '47025'::bigint THEN ' ice-cream promotion'::text
            WHEN trn_promotion_id <> '0'::bigint THEN 'other promotion'::text
            ELSE 'No promotion'::text
        END AS promo_type,
    trn_item_number,
    units,
    gross_amount,
    vat,
    cost_price
   FROM interview.transactions;
RESET search_path;
