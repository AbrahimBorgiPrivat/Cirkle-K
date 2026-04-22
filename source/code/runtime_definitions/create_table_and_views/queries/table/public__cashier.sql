CREATE TABLE IF NOT EXISTS "public"."cashier"
(
    "cashier_id" text NOT NULL,
    "type" text,
    "pno" bigint,
    CONSTRAINT "cashier_pkey" PRIMARY KEY (cashier_id)
);
