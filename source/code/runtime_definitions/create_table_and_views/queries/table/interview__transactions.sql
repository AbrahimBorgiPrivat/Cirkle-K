CREATE TABLE IF NOT EXISTS "interview"."transactions"
(
    "id" bigint NOT NULL,
    "site_number" bigint,
    "trn_transaction_date" date,
    "trn_promotion_id" bigint,
    "trn_item_number" bigint,
    "units" numeric,
    "gross_amount" numeric,
    "vat" numeric,
    "cost_price" numeric,
    CONSTRAINT "transactions_pkey" PRIMARY KEY (id)
);
