#!/usr/bin/python

import time
import praw
import yaml
from pyslack import SlackClient

input = open("storage.txt","r")

with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

#importing config
apitoken = cfg['apitoken'] 
channel = cfg['channel']

#passing API token to pyslack
client = SlackClient(apitoken)

#init PRAW and login
r = praw.Reddit('NewfriendCatcher by hlprimm /u/ajisai v 1.0')
r.login(disable_warning=True)

#ghetto per-instance "database" until i figure yaml out
already_done = str(input.read()).split()

#keywords to search, need to pull these from the yaml too. 
newfriendWords = ['new', 'looking', 'join', 'server']

#don't change below plz
while True:
    print 'Checking for more newfriends...'
    subreddit = r.get_subreddit('civcraft')
    for submission in subreddit.get_new(limit=25):
        op_text = submission.selftext.lower()
        has_newfriend = any(string in op_text for string in newfriendWords)
        flair = submission.author_flair_text
        if submission.id not in already_done and has_newfriend and not flair:
            output = open("storage.txt","a")
            msg = '[NEWFRIEND?] ' + submission.title + submission.short_link
            client.chat_post_message(channel, msg, username='Newfriend Catcher')
            already_done.append(submission.id)
            output.write(submission.id+"\n")
            print 'Sending to Slack!'

        else: print '\033[1m' + submission.title + '\033[0m' + ' does not meet criteria, moving on'
        time.sleep(120);
