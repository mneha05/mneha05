with by_user as (
  select
    user_id,
    max(experiment_arm) as experiment_arm,
    max(case when event_name='feature_view' then 1 else 0 end) as converted
  from {{ ref('stg_events') }}
  group by 1
)
select
  experiment_arm,
  count(*) as users,
  sum(converted) as converters,
  cast(sum(converted) as double)/nullif(count(*),0) as conversion_rate
from by_user
group by 1
