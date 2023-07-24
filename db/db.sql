CREATE TABLE IF NOT EXISTS public.item_count (
	id serial primary key,
	object_class VARCHAR (50) unique not null,
	observed_count int
);