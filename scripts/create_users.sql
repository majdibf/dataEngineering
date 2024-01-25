-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	"name" text NOT NULL,
	id int4 NOT NULL,
	street text NOT NULL,
	city text NOT NULL,
	zip text NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);