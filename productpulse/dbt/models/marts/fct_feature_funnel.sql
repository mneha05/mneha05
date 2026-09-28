with by_user as (
  select
    user_id,
    max(case when event_name='app_open' then 1 else 0 end) as opened,
    max(case when event_name='feature_view' then 1 else 0 end) as viewed_feature,
    max(case when event_name='like' then 1 else 0 end) as liked,
    max(case when event_name='share' then 1 else 0 end) as shared
  from {{ ref('stg_events') }}
  group by 1
)
select
  sum(opened) as app_open_users,
  sum(viewed_feature) as feature_view_users,
  sum(liked) as like_users,
  sum(shared) as share_users,
  cast(sum(viewed_feature) as double) / nullif(sum(opened),0) as feature_adoption,
  cast(sum(liked) as double) / nullif(sum(viewed_feature),0) as feature_to_like,
  cast(sum(shared) as double) / nullif(sum(viewed_feature),0) as feature_to_share
from by_user
