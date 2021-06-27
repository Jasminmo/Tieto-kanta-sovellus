CREATE TABLE "Users" (
  "id" SERIAL PRIMARY KEY,
  "firstname" varchar(100),
  "salted_passwd" varchar,
  "created_at" timestamp,
  "is_admin" boolean
);

CREATE TABLE "Channel" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(100),
  "description" text,
  "created_at" timestamp,
  "is_secret" boolean
);

CREATE TABLE "Secret_Channel_Users" (
  "user_id" int,
  "channel_id" int,
  PRIMARY KEY ("user_id", "channel_id")
);

CREATE TABLE "Channel_Rating" (
  "user_id" int,
  "channel_id" int,
  "rating" int,
  PRIMARY KEY ("user_id", "channel_id")
);

CREATE TABLE "Thread" (
  "id" SERIAL PRIMARY KEY,
  "channel_id" int,
  "owner_id" int,
  "title" varchar(100),
  "created_at" timestamp
);

CREATE TABLE "Message" (
  "id" SERIAL PRIMARY KEY,
  "sender_id" int,
  "thread_id" int,
  "reply_id" int,
  "content" varchar(200),
  "send_at" timestamp
);

CREATE TABLE "Likes" (
  "user_id" int,
  "message_id" int,
  PRIMARY KEY ("user_id", "message_id")
);

ALTER TABLE "Secret_Channel_Users" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Secret_Channel_Users" ADD FOREIGN KEY ("channel_id") REFERENCES "Channel" ("id");

ALTER TABLE "Channel_Rating" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Channel_Rating" ADD FOREIGN KEY ("channel_id") REFERENCES "Channel" ("id");

ALTER TABLE "Thread" ADD FOREIGN KEY ("channel_id") REFERENCES "Channel" ("id");

ALTER TABLE "Thread" ADD FOREIGN KEY ("owner_id") REFERENCES "Users" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("sender_id") REFERENCES "Users" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("thread_id") REFERENCES "Thread" ("id");

ALTER TABLE "Message" ADD FOREIGN KEY ("reply_id") REFERENCES "Message" ("id");

ALTER TABLE "Likes" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "Likes" ADD FOREIGN KEY ("message_id") REFERENCES "Message" ("id");

