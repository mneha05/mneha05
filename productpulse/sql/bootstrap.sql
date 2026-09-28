CREATE SCHEMA IF NOT EXISTS iceberg.productpulse
WITH (location = 's3://warehouse/productpulse/');

CREATE TABLE IF NOT EXISTS iceberg.productpulse.raw_events (
  event_id varchar,
  user_id varchar,
  event_name varchar,
  event_ts timestamp(6) with time zone,
  event_date date,
  session_id varchar,
  country varchar,
  platform varchar,
  experiment_arm varchar,
  feature_name varchar,
  ingested_at timestamp(6) with time zone
)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['day(event_date)']
);
