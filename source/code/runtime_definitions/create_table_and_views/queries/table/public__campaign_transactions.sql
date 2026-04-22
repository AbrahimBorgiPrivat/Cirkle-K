CREATE TABLE IF NOT EXISTS "public"."campaign_transactions"
(
    "campaign_transaction_id" text NOT NULL,
    "campaign_id" bigint,
    "customer_id" text,
    CONSTRAINT "campaign_transactions_pkey" PRIMARY KEY (campaign_transaction_id)
);
