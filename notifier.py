import time
import praw
from pyslack import SlackClient

apitoken = raw_input('Enter your slack API token: ')
channel = raw_input('Enter the slack channel with # before the channel name (example: #random): ')

client = SlackClient(apitoken)

r = praw.Reddit('NewfriendCatcher by hlprimm /u/ajisai v 1.0')

r.login()
already_done = [] 

#keywords to search
newfriendWords = ['new', 'looking', 'join', 'server']

while True:
	subreddit = r.get_subreddit('civcraft')
	for submission in subreddit.get_new(limit=20):
		op_text = submission.selftext.lower()
		has_newfriend = any(string in op_text for string in newfriendWords)
	
		if submission.id not in already_done and has_newfriend:
			msg = '[NEWFRIEND?](%s)' %  submission.title + submission.short_link
			client.chat_post_message(channel, msg, username='NewfriendCatcher')
			already_done.append(submission.id)
	time.sleep(1800);

