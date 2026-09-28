with first_seen as (
  select user_id, min(event_date) as cohort_date
  from {{ ref('stg_events') }}
  group by 1
),
activity as (
  select distinct user_id, event_date from {{ ref('stg_events') }}
),
cohorts as (
  select
    f.cohort_date,
    count(*) as cohort_size,
    count_if(a1.user_id is not null) as d1_retained,
    count_if(a7.user_id is not null) as d7_retained
  from first_seen f
  left join activity a1 on a1.user_id=f.user_id and a1.event_date=f.cohort_date + interval '1' day
  left join activity a7 on a7.user_id=f.user_id and a7.event_date=f.cohort_date + interval '7' day
  group by 1
)
select
  *,
  cast(d1_retained as double)/nullif(cohort_size,0) as d1_retention,
  cast(d7_retained as double)/nullif(cohort_size,0) as d7_retention
from cohorts
