# **NBA Fans Sentiments During the 2020 NBA Finals**

## Overview

See the final visualization [here](https://datastudio.google.com/reporting/3fe2edbd-4219-4925-a899-8e6549fc0c1c).

I scrapped and analyzed gamethread comments from the LA Lakers and Miami Heat's subreddits for each game of the 2019-2020 NBA Finals.

* Can we use sentiment analysis to track fans reactions to their teams performance during a game?
* Are team reactions simply informed by fandom? Do we see completely opposite reactions from opposing teams?

My hypothesis was reactions would be moderately to strongly negatively correlated, as sports are zero-sum by nature I assumed reactions would similarly follow. 

This was driven in part by anecdotal evidence: during games I liked to watch both team subreddits and noticed completely opposite reactions from ref calls and mundane plays. I wanted to know if this anecdote would hold across an entire game and series.   

### Observations & future improvements

While I did find moments of negative correlation, the pattern does not hold for entire games. 

I also calculated the pearson correlation coefficient for each game, shown below.

| Game | Correlation Coefficient |
|------|-------------------------|
| 1    | 0.3132687187            |
| 2    | 0.03161549603           |
| 3    | -0.1679602034           |
| 4    | 0.07073773985           |
| 5    | 0.05096016136           |
| 6    | -0.2017694083           |

Further analysis should be done to explain the divergence, but one hypothesis could be each subreddit focuses on different aspects of the game due to their fandom, and ony infrequent big plays or ref decisions cause polarized reactions.    

### Data sources
Fan reactions were taken from the team specific game threads (/r/Lakers and /r/Heat).

I used [nba_api](https://github.com/swar/nba_api) to get play by play data for each game. This provided the exact tip-off time, as well as scores mapped to real time.

## Process  

All data processing and scripts were built and ran on a GCP cloud instance using a combination of GCE, GCS and GCF and BigQuery.

### Comment Scraping
I used [praw](https://github.com/praw-dev/praw) to get all comments from a given reddit thread url. Each comment was written to its own blob in a google cloud storage bucket.

### Sentiment Analysis

Prior to running the comment scraper, I set up a cloud function triggered on the creation of new objects in my bucket. 

This enabled parallel processing on the comments, greatly speeding up the run time. 

I used Google's natural language API to calculate the sentiment score.

### SQL Cleaning

After loading the processed comments into BigQuery, I used SQL to calculate the minutes since tipoff for each comment. 

Then I aggregated the comments into 5 minute periods and got the average sentiment for that period.

### Visualization 

The visualization was built in Google Data Studio. 

