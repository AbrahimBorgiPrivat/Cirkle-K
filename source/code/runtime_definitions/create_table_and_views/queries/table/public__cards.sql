CREATE TABLE IF NOT EXISTS "public"."cards"
(
    "card_id" text NOT NULL,
    "card_number" text,
    "card_type" text,
    "loyalty_id" text,
    CONSTRAINT "cards_pkey" PRIMARY KEY (card_id)
);
