CREATE TABLE IF NOT EXISTS "public"."transactions"
(
    "transaction_id" text NOT NULL,
    "timestamp" timestamp without time zone,
    "cashier_id" text,
    "card_id" text,
    "context" jsonb,
    CONSTRAINT "transactions_pkey" PRIMARY KEY (transaction_id)
);
