"""Gets latest tweets about doge and stores them in a DB.

Fetches and stores the latest tweets from Elon Musk about dogecoin in a SQL database.

To run:
    python3 twitter.py
"""

import os
import pickle
import psycopg2
import re
import tweepy
from datetime import datetime


NAME = None
USER = None
PASS = None
HOST = '127.0.0.1'
PORT = '5432'

if(os.environ['PWD'].find("app") >= 0):
    db_url_pattern = """
        postgres://(?P<user>\w*):(?P<pass>\w*)@(?P<host>[\w\-\.]*):(?P<port>\d*)\/(?P<name>\w*)
    """
    m = re.search(re.compile(db_url_pattern, re.MULTILINE | re.VERBOSE),
                os.environ['DATABASE_URL'])

    NAME = m.group('name')
    USER = m.group('user')
    PASS = m.group('pass')
    HOST = m.group('host')
    PORT = m.group('port')
else:
    NAME = os.environ['NAME']
    USER = os.environ['USER']
    PASS = os.environ['PASS']


class Twitter:
    def __init__(self):
        """ Initializes twitter API authentication. """
        # Environment vars set in activate script
        tokens = [
            os.environ['consumer_key'],
            os.environ['consumer_secret'],
            os.environ['access_token'],
            os.environ['access_token_secret']
        ]
        assert all(tokens), f"Environment variables not set: {tokens}"
        auth = tweepy.OAuthHandler(tokens[0], tokens[1])
        auth.set_access_token(tokens[2], tokens[3])
        assert auth, f"Twitter auth not set: {auth}."
        self._api = tweepy.API(auth)

    def _get_tweets(self):
        """Gets tweets from twitter.

        Returns:
            tweets: A list of tweets fetched from twitter.
        """
        tweets = []

        for page_num, page in enumerate(tweepy.Cursor(
            self._api.user_timeline,
            screen_name="elonmusk",
            count=50,
            tweet_mode="extended").pages(1)):
            print(f"Page num: {page_num}")
            for status in page:
                tweets.append(status)

        print(f"Found {len(tweets)} tweets.")
        return tweets

    def _filter_tweets(self, tweets):
        """ Filters tweets for tweets containing the word doge.

        Args:
            tweets: The tweets to filter.

        Returns:
            filtered: The filtered tweets.
        """
        doge_pattern = r"""(?P<doge>[dD4][oO0][gG][eE3])"""
        doge_re = re.compile(doge_pattern, re.MULTILINE | re.IGNORECASE)
        filtered = []
        for tweet in tweets:

            if(doge_re.search(tweet.full_text)):
                # Find timestamp of the day excluding time of day.
                tweet_date = tweet.created_at.date()
                tweet_date = int(datetime(
                    tweet_date.year,
                    tweet_date.month,
                    tweet_date.day).timestamp())

                filtered.append([tweet_date, tweet.full_text])
        print(f"Found {len(filtered)} tweets about doge.")
        return filtered

    def _create_table(self):
        """ Creates table to store tweets about doge. """
        sql = """CREATE TABLE IF NOT EXISTS tweets(
            id SERIAL PRIMARY KEY,
            ts NUMERIC NOT NULL,
            tweet text NOT NULL,
            UNIQUE (ts, tweet)
            )"""
        conn = None
        try:
            conn = psycopg2.connect(f"dbname={NAME} user={USER}")
            # create a new cursor
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def _insert_items(self, items):
        """ Insert multiple values into a table.

        Args:
            items: A list of lists to insert.
        Returns:
            new_tweets: The number of tweets inserted into the DB.
        """
        sql = "INSERT INTO tweets(ts, tweet) VALUES(%s, %s) ON CONFLICT DO NOTHING;"
        num_tweets_sql = "select COUNT(*) from tweets;"
        conn = None
        new_tweets = 0
        try:
            conn = psycopg2.connect(f"dbname={NAME} user={USER}")
            # create a new cursor
            cur = conn.cursor()
            cur.execute(num_tweets_sql)
            init_len = int(cur.fetchone()[0])

            # execute the INSERT statement
            cur.executemany(sql,items)

            # commit the changes to the database
            conn.commit()
            cur.execute(num_tweets_sql)
            new_len = int(cur.fetchone()[0])
            new_tweets = new_len - init_len

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return new_tweets

    def run(self):
        """ Finds tweets about doge. """
        self._create_table()
        tweets = self._filter_tweets(self._get_tweets())
        if(len(tweets) > 0):
            num_inserted_tweets = self._insert_items(tweets[::-1])
            print(f"Added {num_inserted_tweets} tweets.")


if __name__ == "__main__":
    Twitter().run()