CREATE TABLE IF NOT EXISTS "datafordeler"."dagi_storkreds"
(
    "id" bigint NOT NULL,
    "storkredsnummer" bigint,
    "navn" text,
    "gml_id" text,
    "dag_id" text,
    "id_namespace" text,
    "status" text,
    "landekode" text,
    "geometristatus" text,
    "skala" text,
    "geometri" text,
    "virkning_fra" timestamp without time zone,
    "virkning_til" timestamp without time zone,
    "virkningsaktoer" text,
    "registrering_fra" timestamp without time zone,
    "registrering_til" timestamp without time zone,
    "registreringsaktoer" text,
    "datafordeler_opdateringstid" timestamp without time zone,
    "updatetime" timestamp without time zone,
    "createdtime" timestamp without time zone,
    CONSTRAINT "dagi_storkreds_pkey" PRIMARY KEY (id)
);
