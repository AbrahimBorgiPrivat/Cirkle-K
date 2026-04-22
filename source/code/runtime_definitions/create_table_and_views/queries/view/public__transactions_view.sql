SET search_path TO "public", public;
DROP VIEW IF EXISTS "public"."transactions_view";
CREATE OR REPLACE VIEW "public"."transactions_view" AS
SELECT transactions.transaction_id,
    transactions."timestamp" AS full_timestamp,
    EXTRACT(days FROM transactions."timestamp" - loyality_customers.signed_up) AS days_after_signup,
    transactions."timestamp"::date AS date_only,
    EXTRACT(hour FROM transactions."timestamp") AS hour_only,
    EXTRACT(minute FROM transactions."timestamp") AS minute_only,
    transactions.cashier_id,
    transactions.card_id,
    loyality_customers.loyalty_id AS cust_id,
    transactions.context
   FROM transactions
     JOIN cards ON cards.card_id = transactions.card_id
     JOIN loyality_customers ON loyality_customers.loyalty_id = cards.loyalty_id;
RESET search_path;
