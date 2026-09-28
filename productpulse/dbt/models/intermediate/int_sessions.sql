select
    session_id,
    user_id,
    min(event_ts) as session_start,
    max(event_ts) as session_end,
    date_diff('second', min(event_ts), max(event_ts)) as session_seconds,
    count(*) as event_count,
    max(case when event_name = 'feature_view' then 1 else 0 end) as used_feature
from {{ ref('stg_events') }}
group by 1,2
