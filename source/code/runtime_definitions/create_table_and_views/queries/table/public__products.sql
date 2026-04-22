CREATE TABLE IF NOT EXISTS "public"."products"
(
    "product_id" bigint NOT NULL,
    "name" text,
    "type" text,
    "quantifier" text,
    "standard_price" boolean,
    "price" double precision,
    CONSTRAINT "products_pkey" PRIMARY KEY (product_id)
);
