CREATE TABLE IF NOT EXISTS "interview"."item_master"
(
    "item_number" bigint NOT NULL,
    "item_name" text,
    "item_subcategory" text,
    CONSTRAINT "item_master_pkey" PRIMARY KEY (item_number)
);
