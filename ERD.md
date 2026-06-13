CREATE TABLE "users" (

"id" uuid PRIMARY KEY,

"email" varchar UNIQUE,

"username" varchar UNIQUE,

"full\_name" varchar,

"avatar\_url" text,

"role" varchar,

"email\_verified" boolean,

"created\_at" timestamp,

"updated\_at" timestamp

);

CREATE TABLE "sessions" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"token" varchar,

"expires\_at" timestamp,

"ip\_address" varchar,

"user\_agent" text,

"created\_at" timestamp

);

CREATE TABLE "accounts" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"provider" varchar,

"provider\_account\_id" varchar,

"access\_token" text,

"refresh\_token" text,

"created\_at" timestamp

);

CREATE TABLE "countries" (

"id" uuid PRIMARY KEY,

"name" varchar,

"iso\_code" varchar,

"capital" varchar,

"population" bigint,

"area\_km2" bigint,

"currency" varchar,

"continent" varchar,

"flag\_url" text,

"latitude" decimal,

"longitude" decimal,

"description" text,

"created\_at" timestamp,

"updated\_at" timestamp

);

CREATE TABLE "states" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"name" varchar,

"code" varchar,

"description" text

);

CREATE TABLE "cities" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"state\_id" uuid,

"name" varchar,

"population" bigint,

"latitude" decimal,

"longitude" decimal,

"description" text,

"created\_at" timestamp

);

CREATE TABLE "landmarks" (

"id" uuid PRIMARY KEY,

"city\_id" uuid,

"name" varchar,

"category" varchar,

"latitude" decimal,

"longitude" decimal,

"description" text,

"created\_at" timestamp

);

CREATE TABLE "place\_facts" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"category" varchar,

"title" varchar,

"content" text,

"created\_at" timestamp

);

CREATE TABLE "images" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"pexels\_id" varchar,

"image\_url" text,

"photographer" varchar,

"source" varchar,

"created\_at" timestamp

);

CREATE TABLE "generated\_guides" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"title" varchar,

"content" text,

"generated\_by" varchar,

"created\_at" timestamp

);

CREATE TABLE "bookmarks" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"created\_at" timestamp

);

CREATE TABLE "search\_history" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"search\_query" text,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"created\_at" timestamp

);

CREATE TABLE "conversations" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"title" varchar,

"created\_at" timestamp,

"updated\_at" timestamp

);

CREATE TABLE "messages" (

"id" uuid PRIMARY KEY,

"conversation\_id" uuid,

"role" varchar,

"content" text,

"model\_used" varchar,

"created\_at" timestamp

);

CREATE TABLE "agents" (

"id" uuid PRIMARY KEY,

"name" varchar,

"description" text,

"system\_prompt" text,

"created\_at" timestamp

);

CREATE TABLE "agent\_runs" (

"id" uuid PRIMARY KEY,

"agent\_id" uuid,

"user\_id" uuid,

"conversation\_id" uuid,

"status" varchar,

"started\_at" timestamp,

"completed\_at" timestamp

);

CREATE TABLE "tool\_calls" (

"id" uuid PRIMARY KEY,

"run\_id" uuid,

"tool\_name" varchar,

"input" json,

"output" json,

"created\_at" timestamp

);

CREATE TABLE "embeddings" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"source\_text" text,

"embedding" vector,

"created\_at" timestamp

);

CREATE TABLE "cache\_entries" (

"id" uuid PRIMARY KEY,

"cache\_key" varchar,

"cache\_data" json,

"expires\_at" timestamp

);

CREATE TABLE "quizzes" (

"id" uuid PRIMARY KEY,

"country\_id" uuid,

"city\_id" uuid,

"landmark\_id" uuid,

"title" varchar,

"difficulty" varchar,

"created\_at" timestamp

);

CREATE TABLE "quiz\_questions" (

"id" uuid PRIMARY KEY,

"quiz\_id" uuid,

"question" text,

"option\_a" text,

"option\_b" text,

"option\_c" text,

"option\_d" text,

"correct\_answer" varchar

);

CREATE TABLE "quiz\_attempts" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"quiz\_id" uuid,

"score" int,

"completed\_at" timestamp

);

CREATE TABLE "analytics\_events" (

"id" uuid PRIMARY KEY,

"user\_id" uuid,

"event\_type" varchar,

"metadata" json,

"created\_at" timestamp

);

ALTER TABLE "sessions" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "accounts" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "states" ADD FOREIGN KEY ("country\_id") REFERENCES "countries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cities" ADD FOREIGN KEY ("country\_id") REFERENCES "countries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cities" ADD FOREIGN KEY ("state\_id") REFERENCES "states" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "landmarks" ADD FOREIGN KEY ("city\_id") REFERENCES "cities" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "generated\_guides" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "bookmarks" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "search\_history" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "conversations" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "messages" ADD FOREIGN KEY ("conversation\_id") REFERENCES "conversations" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent\_runs" ADD FOREIGN KEY ("agent\_id") REFERENCES "agents" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent\_runs" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent\_runs" ADD FOREIGN KEY ("conversation\_id") REFERENCES "conversations" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tool\_calls" ADD FOREIGN KEY ("run\_id") REFERENCES "agent\_runs" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz\_questions" ADD FOREIGN KEY ("quiz\_id") REFERENCES "quizzes" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz\_attempts" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz\_attempts" ADD FOREIGN KEY ("quiz\_id") REFERENCES "quizzes" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "analytics\_events" ADD FOREIGN KEY ("user\_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
