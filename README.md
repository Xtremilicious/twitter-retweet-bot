# Twitter-Retweet-Bot
A Twitter retweet bot using Twitter API and Tweepy built with Python. Supports multiple keywords/hashtags.

What You Need & Need to Know
----------

* [Tweepy](http://www.tweepy.org/) - An easy-to-use Python library for accessing the Twitter API.

* Make sure you fully understand [Twitter's Rules on Automation](https://support.twitter.com/articles/76915). Play nice. Don't spam! 

Setup
----------

Install all dependencies

```
pip install -r requirements.txt
```

Creates a `.env` file with all environment variables like the `.env.example` file.

Instructions
----------

* Out of general OS hygiene, create a new directory to contain all of your retweet bot files.

`mkdir retweet-bot`

* Create a new [Twitter Application](https://apps.twitter.com/app/new). This is where you'll generate your keys, tokens, and secrets.
* Fill in your keys, tokens, and secrets in the .env file.
* Check comments in retweet.py to tweak the retweet bot to your liking.
* The example demonstrates a single hashtag value, but you can tweak the code to search multiple hashtags. Example:

 `q='%23art%20OR%20%23music' will search #art OR #music`
* Run your retweet.py script. Enjoy! 

`python retweet.py`

Additional Information
----------
* Note: Make sure that your retweet.py and .env files are, obviously, in the same directory.
* Create a [Cron Job](https://code.tutsplus.com/tutorials/scheduling-tasks-with-cron-jobs--net-8800) or use [Task Scheduler](https://technet.microsoft.com/en-us/library/cc748993(v=ws.11).aspx) to automate this script.
* Use Heroku for hosting the scripts and assign a dyno to run this script continuously.
* Consider using a Raspberry Pi to host your retweet bot, so it's always on and always running. :)
