CREATE TABLE IF NOT EXISTS "datafordeler"."dar_adressepunkt"
(
    "id" text NOT NULL,
    "pos" text,
    "oprindelse_kilde" text,
    "oprindelse_nojagtighedsklasser" text,
    "oprindelse_registrering" text,
    "oprindelse_teknisk_standard" text,
    "id_namespace" text,
    "status" text,
    "virkning_fra" timestamp without time zone,
    "virkning_til" timestamp without time zone,
    "virkningsaktoer" text,
    "registrering_fra" timestamp without time zone,
    "registrering_til" timestamp without time zone,
    "registreringsaktoer" text,
    "datafordeler_opdateringstid" timestamp without time zone,
    "updatetime" timestamp without time zone,
    "createdtime" timestamp without time zone,
    CONSTRAINT "dar_adressepunkt_pkey" PRIMARY KEY (id)
);
