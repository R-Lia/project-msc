drop table items;

create table items (
	"id" integer PRIMARY KEY AUTOINCREMENT,
	"name" varchar(30) NOT NULL,
	"description" varchar(255) NOT NULL,
	"quantity" integer NOT NULL,
	"price" decimal NOT NULL,
	"listname" varchar(60) NOT NULL REFERENCES "lists" ("name")
);

