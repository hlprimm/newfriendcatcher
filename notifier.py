import time
import praw
from pyslack import SlackClient

#add your api token, get one here: https://senntisten.slack.com/services/new/bot
client = SlackClient('SLACK API TOKEN')

r = praw.Reddit('NewfriendCatcher by hlprimm /u/ajisai v 1.0')

r.login()
already_done = [] 

#keywords to search
newfriendWords = ['new', 'looking', 'join', 'server']

while True:
	subreddit = r.get_subreddit('civcraft')
	for submission in subreddit.get_hot(limit=100):
		op_text = submission.selftext.lower()
		has_newfriend = any(string in op_text for string in newfriendWords)
	
		if submission.id not in already_done and has_newfriend:
			msg = '[NEWFRIEND?](%s)' % submission.short_link
			#Change DESTINATIONCHANNEL to channel you want the message to go. 
			#Change NewfriendCatcher to whatever your bot name is on Slack.
			client.chat_post_message('#DESTINATIONCHANNEL', msg, username='NewfriendCatcher')
			already_done.append(submission.id)
	time.sleep(1800);

