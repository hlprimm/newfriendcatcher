#!/usr/bin/python

import time
import praw
import yaml
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from pyslack import SlackClient

input = open("output.txt","r")

with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

#google sheets with gspread
json_key = json.load(open('newfriendcatcher.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], bytes(json_key['private_key'], 'utf-8'), scope)
gc = gspread.authorize(credentials)
sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/1BKBsGCAKTRi_aPmzIoEO6FsJF8HDxMEw5eh7L37BJvw/edit#gid=0')


#importing config
apitoken = cfg['apitoken'] 
channel = cfg['channel']
username = cfg['redditusername']
password = cfg ['redditpassword']

print(list)
#passing API token to pyslack
client = SlackClient(apitoken)

#init PRAW and login
r = praw.Reddit('NewfriendCatcher by hlprimm /u/ajisai v 1.0')
r.login(username,password,disable_warning=True)

#ghetto per-instance "database" until i figure yaml out
already_done = str(input.read()).split()

#keywords to search, need to pull these from the yaml too. 
tier1 = cfg["tier1"]
tier2 = cfg["tier2"]

#don't change below plz
while True:
    print ('Checking for more newfriends...')
    subreddit = r.get_subreddit('civcraft')
    for submission in subreddit.get_new(limit=10):
        op_text = submission.selftext.lower()
        has_newfriend = False
        if any(string in op_text for string in tier1): has_newfriend = True
        for x in range(len(tier2)):
            if tier2[x] in op_text or submission.title:
                for y in range(len(tier2)):
                    if tier2[y] in op_text and tier2[y] is not tier2[x]: has_newfriend = False

        flair = submission.author_flair_text
        if submission.id not in already_done and has_newfriend and not flair:
            output = open("output.txt","a")
            msg = '[NEWFRIEND?] ' + submission.title + submission.short_link
            client.chat_post_message(channel, msg, username='Newfriend Catcher')
            already_done.append(submission.id)
            output.write(submission.id+"\n")
            print ('Sending to Slack!')
            time.sleep(120)

        else:
            print ('\033[1m' + submission.title + '\033[0m' + ' does not meet criteria, moving on')
            time.sleep(10)
