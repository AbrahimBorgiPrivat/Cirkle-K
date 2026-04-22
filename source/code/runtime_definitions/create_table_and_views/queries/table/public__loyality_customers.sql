CREATE TABLE IF NOT EXISTS "public"."loyality_customers"
(
    "loyalty_id" text NOT NULL,
    "name" text,
    "phone" text,
    "email" text,
    "country" text,
    "primary_station" bigint,
    "segmentationgroup" bigint,
    "signed_up" timestamp without time zone,
    "perm_notify" boolean,
    "perm_email" boolean,
    "perm_sms" boolean,
    "perm_survey" boolean,
    CONSTRAINT "loyality_customers_pkey" PRIMARY KEY (loyalty_id)
);
