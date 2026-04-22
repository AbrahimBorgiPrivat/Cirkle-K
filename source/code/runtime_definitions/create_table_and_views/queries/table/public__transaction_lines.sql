CREATE TABLE IF NOT EXISTS "public"."transaction_lines"
(
    "id" text NOT NULL,
    "transaction_id" text,
    "product_id" bigint,
    "product" text,
    "price" double precision,
    "discount" double precision,
    "quantity" bigint,
    "total" double precision,
    "campaign_transaction_id" text,
    "context" jsonb,
    CONSTRAINT "transaction_lines_pkey" PRIMARY KEY (id)
);
