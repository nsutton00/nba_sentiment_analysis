WITH
  staging AS (
  SELECT
    CAST(timestamp AS INT64) AS timestamp_int,
    (sentiment*magnitude) AS sentiment_score,
    *
  FROM
    `nba-sentiments.comment_sentiment.j9eu26_g6_lakers` 
   #filter out deleted comments and comments that were too ambiguious to receive a sentiment score 
   WHERE text NOT IN ('[deleted]', ' [deleted] ', '[deleted]\n') AND (sentiment != 0 AND magnitude != 0)),
  #given the tip off time, calculate minutes since for each comment 
  game_time_diff AS (
  SELECT
    #must be in utc
    TIMESTAMP_DIFF(TIMESTAMP_SECONDS(timestamp_int), TIMESTAMP("2020-10-12 1:11:00-00"), MINUTE) AS time_since,
    sentiment_score,
    sentiment,
    magnitude,
    text
  FROM
    staging
  ORDER BY
    time_since ASC),
#break comments into 5 minute periods, get the average magnitude and sentiment for each period
  group_by_time AS (
SELECT
  ROUND(AVG(sentiment_score),1) AS sentiment_score,
  ROUND(AVG(sentiment),1) AS sentiment_avg,
  ROUND(AVG(magnitude),1) AS magnitude_avg,
  MIN(time_since) AS time_since,
  ARRAY_AGG(text) as comments
FROM
  game_time_diff
GROUP BY
  DIV(time_since - 1, 5)
ORDER BY
  time_since ASC, sentiment_score desc
)

#returning array legnth as sanity check; you'd expect number of comments to be high during expected gametime
SELECT time_since, sentiment_score, ARRAY_LENGTH(comments) FROM group_by_time order by time_since
    