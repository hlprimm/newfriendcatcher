import time
import praw
from pyslack import SlackClient

client = SlackClient('xoxb-8778264791-9vC1DJEv8939xFHiUJqktn3c')



r = praw.Reddit('NewfriendCatcher by hlprimm /u/ajisai v 1.0')

r.login()
already_done = [] 

newfriendWords = ['new', 'looking', 'join', 'server']

while True:
	subreddit = r.get_subreddit('civcraft')
	for submission in subreddit.get_hot(limit=100):
		op_text = submission.selftext.lower()
		has_newfriend = any(string in op_text for string in newfriendWords)
	
		if submission.id not in already_done and has_newfriend:
			msg = '[NEWFRIEND?](%s)' % submission.short_link
			client.chat_post_message('#newfriends', msg, username='newfriendcatcher')
			already_done.append(submission.id)
	time.sleep(1800);

