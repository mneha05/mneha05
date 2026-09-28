with daily as (
  select
    event_date,
    count(distinct user_id) as dau,
    count(distinct case when event_name='feature_view' then user_id end) as feature_users,
    count(distinct session_id) as sessions,
    count(*) as events
  from {{ ref('stg_events') }}
  group by 1
),
windowed as (
  select
    d1.*,
    (
      select count(distinct e.user_id)
      from {{ ref('stg_events') }} e
      where e.event_date between d1.event_date - interval '29' day and d1.event_date
    ) as mau_30d
  from daily d1
)
select
  *,
  cast(dau as double) / nullif(mau_30d,0) as dau_mau,
  cast(feature_users as double) / nullif(dau,0) as feature_adoption
from windowed
