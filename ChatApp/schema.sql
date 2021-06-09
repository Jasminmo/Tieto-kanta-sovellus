DROP TABLE IF EXISTS "messages";
DROP TABLE IF EXISTS "threads";
DROP TABLE IF EXISTS "channels";
DROP TABLE IF EXISTS "admins";
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "firstname" varchar unique not null,
  "lastname" varchar not null,
  "username" varchar not null,
  "salted_passwd" varchar not null,
  "admin" boolean not null,
  "created_at" timestamp not null default now()
);

CREATE TABLE "channels" (
  "id" SERIAL PRIMARY KEY,
  "topic" varchar not null,
  "owner_id" int not null,
  "created_at" timestamp not null default now()
);

CREATE TABLE "threads" (
  "id" SERIAL PRIMARY KEY,
  "channel_id" int not null,
  "owner_id" int not null,
  "title" varchar not null,
  "created_at" timestamp not null default now()
);

CREATE TABLE "messages" (
  "id" SERIAL PRIMARY KEY,
  "thread_id" int not null,
  "sender_id" int not null,
  "reply_id" int,
  "content" varchar not null,
  "sent" timestamp not null default now()
);

ALTER TABLE "channels" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "threads" ADD FOREIGN KEY ("channel_id") REFERENCES "channels" ("id");

ALTER TABLE "threads" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("thread_id") REFERENCES "threads" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("sender_id") REFERENCES "users" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("reply_id") REFERENCES "messages" ("id");
