CREATE TABLE IF NOT EXISTS "public"."stations"
(
    "pno" bigint NOT NULL,
    "vat" bigint,
    "name" text,
    "address" text,
    "zipcode" text,
    "city" text,
    "startdate" text,
    "enddate" text,
    CONSTRAINT "stations_pkey" PRIMARY KEY (pno)
);
