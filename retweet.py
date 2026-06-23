import os
import sys
import time
import random
import json
import urllib.error
import urllib.parse
import urllib.request
import tweepy
from dotenv import load_dotenv
from termcolor import colored

#To make the .env file accessible as the source of environment variables
load_dotenv()

#Accessing credentials from .env file
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
RETWEET_BACKEND = os.getenv("RETWEET_BACKEND", "twitter").lower()
XQUIK_API_KEY = os.getenv("XQUIK_API_KEY")
XQUIK_ACCOUNT = os.getenv("XQUIK_ACCOUNT")
XQUIK_API_BASE = os.getenv("XQUIK_API_BASE", "https://xquik.com/api/v1")

#Search Twitter for tweets with this keyword
#Put multiple keywords with 'OR' in between
#Example: search = '#keywordToSearch OR #keywordToSearch2'
search = '#keywordToSearch'

#Maximum limit of tweets to be interacted with
maxNumberOfTweets = 500

#To keep track of tweets published
count = 0

def require_env(name, value):
    if not value:
        raise ValueError(name + " is required")
    return value

def twitter_api():
    #Setting credentials to access Twitter API
    auth = tweepy.OAuthHandler(
        require_env("CONSUMER_KEY", CONSUMER_KEY),
        require_env("CONSUMER_SECRET", CONSUMER_SECRET),
    )
    auth.set_access_token(
        require_env("ACCESS_TOKEN", ACCESS_TOKEN),
        require_env("ACCESS_TOKEN_SECRET", ACCESS_TOKEN_SECRET),
    )

    #Calling API using Tweepy
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def xquik_request(path, method="POST", body=None):
    payload = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        XQUIK_API_BASE.rstrip("/") + path,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": require_env("XQUIK_API_KEY", XQUIK_API_KEY),
        },
        method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        response_body = response.read().decode("utf-8")
    return json.loads(response_body) if response_body else {}

def search_tweets():
    if RETWEET_BACKEND == "twitter":
        api = twitter_api()
        return tweepy.Cursor(api.search, search).items(maxNumberOfTweets)
    if RETWEET_BACKEND == "xquik":
        query = urllib.parse.urlencode({
            "q": search,
            "limit": str(maxNumberOfTweets),
        })
        response = xquik_request("/x/tweets/search?" + query, method="GET")
        return response.get("tweets", [])
    raise ValueError("RETWEET_BACKEND must be twitter or xquik")

def tweet_id(tweet):
    if isinstance(tweet, dict):
        identifier = tweet.get("id") or tweet.get("tweet_id")
    else:
        identifier = getattr(tweet, "id", None)
    if not identifier:
        raise ValueError("tweet id is required")
    return str(identifier)

def tweet_author(tweet):
    if isinstance(tweet, dict):
        author = tweet.get("author")
        if isinstance(author, dict):
            return str(author.get("username") or author.get("user_name") or "unknown")
        return "unknown"
    return tweet.user.screen_name

def retweet(tweet):
    if RETWEET_BACKEND == "twitter":
        tweet.retweet()
        return
    xquik_request(
        "/x/tweets/" + tweet_id(tweet) + "/retweet",
        body={"account": require_env("XQUIK_ACCOUNT", XQUIK_ACCOUNT)},
    )

print(colored('Retweet Bot Started!', 'green'))

try:
    for tweet in search_tweets():
        try:
            print(colored('Found tweet by @' + tweet_author(tweet), 'cyan'))

            #Publishing retweet
            retweet(tweet)

            #Updating count for each successfull retweet
            count = count + 1
            print(colored('Retweet #' + str(count) + ' published successfully.', 'green'))

            #Random wait time
            timeToWait = random.randint(95, 115)
            print("Waiting for "+ str(timeToWait) + " seconds")
            for remaining in range(timeToWait, -1, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\rOnwards to next tweet!\n")

        except tweepy.TweepError as e:
            print('Error: ' + e.args[0][0]['message'])
        except urllib.error.HTTPError as e:
            print('Xquik HTTP Error (' + str(e.code) + '): ' + e.read().decode('utf-8'))
        except StopIteration:
            break
except urllib.error.HTTPError as e:
    print('Xquik HTTP Error (' + str(e.code) + '): ' + e.read().decode('utf-8'))
except ValueError as e:
    print('Error: ' + str(e))
