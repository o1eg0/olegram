-- migrations/001_init.sql
CREATE DATABASE IF NOT EXISTS stats;

CREATE TABLE stats.events
(
    event_date   Date          DEFAULT toDate(event_time),
    event_time   DateTime64(3, 'UTC'),
    event_type   Enum8('view' = 1, 'like' = 2, 'comment' = 3),
    post_id      UUID,
    user_id      String
) ENGINE = MergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (post_id, event_date, event_type);

-- агрегация «пост-день»
CREATE MATERIALIZED VIEW stats.post_daily_agg ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (post_id, event_date)
AS
SELECT
    event_date,
    post_id,
    sum(event_type = 1) AS views,
    sum(event_type = 2) AS likes,
    sum(event_type = 3) AS comments
FROM stats.events
GROUP BY
    event_date,
    post_id;

-- агрегация «пользователь-день»
CREATE MATERIALIZED VIEW stats.user_daily_agg ENGINE = SummingMergeTree
PARTITION BY toYYYYMM(event_date)
ORDER BY (user_id, event_date)
AS
SELECT
    event_date,
    user_id,
    sum(event_type = 1) AS views,
    sum(event_type = 2) AS likes,
    sum(event_type = 3) AS comments
FROM stats.events
GROUP BY
    event_date,
    user_id;
