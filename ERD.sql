CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar UNIQUE,
  "username" varchar UNIQUE,
  "full_name" varchar,
  "avatar_url" text,
  "role" varchar,
  "email_verified" boolean,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "sessions" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "token" varchar,
  "expires_at" timestamp,
  "ip_address" varchar,
  "user_agent" text,
  "created_at" timestamp
);

CREATE TABLE "accounts" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "provider" varchar,
  "provider_account_id" varchar,
  "access_token" text,
  "refresh_token" text,
  "created_at" timestamp
);

CREATE TABLE "countries" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "iso_code" varchar,
  "capital" varchar,
  "population" bigint,
  "area_km2" bigint,
  "currency" varchar,
  "continent" varchar,
  "flag_url" text,
  "latitude" decimal,
  "longitude" decimal,
  "description" text,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "states" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "name" varchar,
  "code" varchar,
  "description" text
);

CREATE TABLE "cities" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "state_id" uuid,
  "name" varchar,
  "population" bigint,
  "latitude" decimal,
  "longitude" decimal,
  "description" text,
  "created_at" timestamp
);

CREATE TABLE "landmarks" (
  "id" uuid PRIMARY KEY,
  "city_id" uuid,
  "name" varchar,
  "category" varchar,
  "latitude" decimal,
  "longitude" decimal,
  "description" text,
  "created_at" timestamp
);

CREATE TABLE "place_facts" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "category" varchar,
  "title" varchar,
  "content" text,
  "created_at" timestamp
);

CREATE TABLE "images" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "pexels_id" varchar,
  "image_url" text,
  "photographer" varchar,
  "source" varchar,
  "created_at" timestamp
);

CREATE TABLE "generated_guides" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "title" varchar,
  "content" text,
  "generated_by" varchar,
  "created_at" timestamp
);

CREATE TABLE "bookmarks" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "created_at" timestamp
);

CREATE TABLE "search_history" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "search_query" text,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "created_at" timestamp
);

CREATE TABLE "conversations" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "title" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "messages" (
  "id" uuid PRIMARY KEY,
  "conversation_id" uuid,
  "role" varchar,
  "content" text,
  "model_used" varchar,
  "created_at" timestamp
);

CREATE TABLE "agents" (
  "id" uuid PRIMARY KEY,
  "name" varchar,
  "description" text,
  "system_prompt" text,
  "created_at" timestamp
);

CREATE TABLE "agent_runs" (
  "id" uuid PRIMARY KEY,
  "agent_id" uuid,
  "user_id" uuid,
  "conversation_id" uuid,
  "status" varchar,
  "started_at" timestamp,
  "completed_at" timestamp
);

CREATE TABLE "tool_calls" (
  "id" uuid PRIMARY KEY,
  "run_id" uuid,
  "tool_name" varchar,
  "input" json,
  "output" json,
  "created_at" timestamp
);

CREATE TABLE "embeddings" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "source_text" text,
  "embedding" vector,
  "created_at" timestamp
);

CREATE TABLE "cache_entries" (
  "id" uuid PRIMARY KEY,
  "cache_key" varchar,
  "cache_data" json,
  "expires_at" timestamp
);

CREATE TABLE "quizzes" (
  "id" uuid PRIMARY KEY,
  "country_id" uuid,
  "city_id" uuid,
  "landmark_id" uuid,
  "title" varchar,
  "difficulty" varchar,
  "created_at" timestamp
);

CREATE TABLE "quiz_questions" (
  "id" uuid PRIMARY KEY,
  "quiz_id" uuid,
  "question" text,
  "option_a" text,
  "option_b" text,
  "option_c" text,
  "option_d" text,
  "correct_answer" varchar
);

CREATE TABLE "quiz_attempts" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "quiz_id" uuid,
  "score" int,
  "completed_at" timestamp
);

CREATE TABLE "analytics_events" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "event_type" varchar,
  "metadata" json,
  "created_at" timestamp
);

ALTER TABLE "sessions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "accounts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "states" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cities" ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cities" ADD FOREIGN KEY ("state_id") REFERENCES "states" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "landmarks" ADD FOREIGN KEY ("city_id") REFERENCES "cities" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "generated_guides" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "bookmarks" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "search_history" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "conversations" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "messages" ADD FOREIGN KEY ("conversation_id") REFERENCES "conversations" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent_runs" ADD FOREIGN KEY ("agent_id") REFERENCES "agents" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent_runs" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "agent_runs" ADD FOREIGN KEY ("conversation_id") REFERENCES "conversations" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "tool_calls" ADD FOREIGN KEY ("run_id") REFERENCES "agent_runs" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz_questions" ADD FOREIGN KEY ("quiz_id") REFERENCES "quizzes" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz_attempts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "quiz_attempts" ADD FOREIGN KEY ("quiz_id") REFERENCES "quizzes" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "analytics_events" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
