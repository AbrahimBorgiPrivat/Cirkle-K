CREATE TABLE IF NOT EXISTS "public"."segmentationsgroups"
(
    "id" bigint NOT NULL,
    "name" text,
    "description" text,
    "avg_txn_per_month" bigint,
    "product_types" jsonb,
    "peak_hours" bigint[],
    "hour_weights" double precision[],
    "weekday_weights" double precision[],
    CONSTRAINT "segmentationsgroups_pkey" PRIMARY KEY (id)
);
