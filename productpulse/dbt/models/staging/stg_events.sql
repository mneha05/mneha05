{{ config(
    unique_key='event_id',
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
) }}

with ranked as (
    select
        event_id,
        user_id,
        event_name,
        event_ts,
        event_date,
        session_id,
        country,
        platform,
        experiment_arm,
        feature_name,
        ingested_at,
        row_number() over (partition by event_id order by ingested_at desc) as rn
    from {{ source('productpulse', 'raw_events') }}
    {% if is_incremental() %}
      where ingested_at >= coalesce((select max(ingested_at) - interval '2' day from {{ this }}), timestamp '1970-01-01 00:00:00 UTC')
    {% endif %}
)
select * from ranked where rn = 1
