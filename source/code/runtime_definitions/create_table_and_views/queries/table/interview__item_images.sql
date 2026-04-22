CREATE TABLE IF NOT EXISTS "interview"."item_images"
(
    "item_number" bigint NOT NULL,
    "img_url" text,
    CONSTRAINT "item_images_pkey" PRIMARY KEY (item_number)
);
