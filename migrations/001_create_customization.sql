CREATE TABLE IF NOT EXISTS public.customization
(
    cust_id integer NOT NULL DEFAULT nextval('customization_cust_id_seq'::regclass),
    user_id integer,
    timer boolean DEFAULT false,
    CONSTRAINT customization_pkey PRIMARY KEY (cust_id),
    CONSTRAINT customization_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customization
    OWNER to postgres;