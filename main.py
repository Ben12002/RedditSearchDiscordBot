import discord
import os
import praw

token = os.getenv('TOKEN')
client = discord.Client()
reddit = praw.Reddit(
        user_agent = "<user_agent>",          
        client_id = "<client_id>",
        client_secret = "<client_secret>",
        username = "<username>",
        password = "<password>",
        )



HELP_STRING = '''----------- HELP -----------
                 RedditUpdatesBot has 2 features:
                 
                 1. search r/dailyprogrammer:
                    - type either \'$easy\', \'$medium\' or \'$hard\' for a challenge of that difficulty.
                 2. search any subreddit:                 
                   - type \'$search <subreddit_name> <keyword>\'
                     for a post in that subreddit containing that keyword'''


def searchSubreddit(subreddit, keyword):
  sub = reddit.subreddit(subreddit)
  for submission in sub.hot(limit=20):
    if keyword in submission.title:
      outputString = (
        f'''{submission.title} 
      -----------------------------------------
      {submission.url}''')
      return outputString
      
  return("nothing found...")


def dailyChallenge(difficulty):
  sub = reddit.subreddit("dailyprogrammer")
  for submission in sub.hot(limit=30):
    if difficulty in submission.title:
      outputString = (
        f'''{submission.title} 
      -----------------------------------------
      {submission.url}''')
      return outputString
  return("nothing found...")
    



@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  messageString = message.content.lower()
  if message.author == client.user:
    return

  if messageString.startswith("$help"):
    await message.channel.send(HELP_STRING)

  if messageString.startswith("$easy"):
    response = dailyChallenge("Easy")
    await message.channel.send(response)
  
  if messageString.startswith("$medium"):
    response = dailyChallenge("Medium")
    await message.channel.send(response)
  
  if messageString.startswith("$hard"):
    response = dailyChallenge("Hard")
    await message.channel.send(response)
  
  if message.content.startswith("$search"):
    msgList = messageString.split(" ", 2)
    response = searchSubreddit(msgList[1], msgList[2])
    await message.channel.send(response)


    


 
client.run(token)
