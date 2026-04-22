CREATE TABLE IF NOT EXISTS "datafordeler"."dar_adresse"
(
    "id" text NOT NULL,
    "adressebetegnelse" text,
    "dorbetegnelse" text,
    "dorpunkt" text,
    "etagebetegnelse" text,
    "bygningid" text,
    "husnummerid" text,
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
    CONSTRAINT "dar_adresse_pkey" PRIMARY KEY (id)
);
