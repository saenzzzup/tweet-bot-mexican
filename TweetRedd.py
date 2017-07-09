import praw
import tweepy, time
from access import *
from random import randint

def twitter_setup():
	# Authenticate and access using keys:
	auth = tweepy.OAuthHandler(CONSUMER_KEY_TWII, CONSUMER_SECRET_TWII)
	auth.set_access_token(ACCESS_TOKEN_TWII, ACCESS_SECRET_TWII)

	# Return API access:
	api = tweepy.API(auth)
	return api

def reddit_setup():
	# Authenticate and access using keys:
	return praw.Reddit(user_agent='Comment Extraction (by /u/-------)', 
	client_id=CONSUMER_KEY_REDD, 
	client_secret=CONSUMER_SECRET_REDD)


def get_correct_Tweet(twee):

	index = twee[0:].find('\n')

	tweeTwo = twee[:index] + " " + hasstag[randint(0, 2)]

	if len(tweeTwo) > 140:
		tweeTwo = tweeTwo[:140]

	return tweeTwo

if __name__ == '__main__':

	#hasstag list
	hasstag = ["#LexicoMexicano", "#MexicanQuotes", "#Chilango"]

	lenComments = 0

	# Setup Twitter API:
	bot = twitter_setup()
	# Setup Reddit API:
	reddit = reddit_setup()
	# get Reddit submissions:
	submission = reddit.submission(id='2p28m4')

	# Set waiting time:
	secs = 1200

	# Set tweet list:
	try:
		tweetlist = submission.comments.list()
		lenComments = len(tweetlist)-1
		print "Success getting comments"
	except praw.exceptions as e:
		print e

	# Tweet posting:
	for i in range(20):
		# Print tweet:
		tweetToPublish = tweetlist[randint(0, lenComments)]

		tweetText = get_correct_Tweet(tweetToPublish.body)

		print tweetText
		
		# Try to post tweet:
		try:
			bot.update_status(tweetText)
			print("Successfully posted.")
		except tweepy.TweepError as e:
			print(e.reason)

		# Wait till next sentence extraction:
		time.sleep(secs)


