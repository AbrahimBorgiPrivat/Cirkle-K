CREATE TABLE IF NOT EXISTS "public"."campaigns"
(
    "id" bigint NOT NULL,
    "name" text,
    "description" text,
    "product_id" bigint,
    "number" bigint,
    "start_date" date,
    "end_date" date,
    "active" boolean,
    CONSTRAINT "campaigns_pkey" PRIMARY KEY (id)
);
