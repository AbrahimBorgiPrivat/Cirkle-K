CREATE TABLE IF NOT EXISTS "interview"."site_master"
(
    "site_number" bigint NOT NULL,
    "site_name" text,
    "site_city" text,
    "site_postal_code" bigint,
    "site_region" text,
    "site_brand" text,
    "site_format" text,
    CONSTRAINT "site_master_pkey" PRIMARY KEY (site_number)
);
