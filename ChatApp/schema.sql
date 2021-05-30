DROP TABLE IF EXISTS "messages";
DROP TABLE IF EXISTS "threads";
DROP TABLE IF EXISTS "channels";
DROP TABLE IF EXISTS "admins";
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "firstname" varchar,
  "lastname" varchar,
  "username" varchar,
  "salted_passwd" varchar,
  "created_at" timestamp
);

CREATE TABLE "admins" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar,
  "salted_passwd" varchar,
  "created_at" timestamp
);

CREATE TABLE "channels" (
  "id" SERIAL PRIMARY KEY,
  "topic" varchar,
  "created_at" timestamp
);

CREATE TABLE "threads" (
  "id" SERIAL PRIMARY KEY,
  "channel_id" int,
  "owner_id" int,
  "title" varchar,
  "created_at" timestamp
);

CREATE TABLE "messages" (
  "id" SERIAL PRIMARY KEY,
  "thread_id" int,
  "sender_id" int,
  "reply_id" int,
  "content" varchar,
  "sent" timestamp
);

ALTER TABLE "threads" ADD FOREIGN KEY ("channel_id") REFERENCES "channels" ("id");

ALTER TABLE "threads" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("thread_id") REFERENCES "threads" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("sender_id") REFERENCES "users" ("id");

ALTER TABLE "messages" ADD FOREIGN KEY ("reply_id") REFERENCES "messages" ("id");
