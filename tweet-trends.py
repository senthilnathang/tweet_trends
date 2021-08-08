import tweepy
import pandas as pd
import sys
import json
import csv
consumer_key = 'YOURKEY'
consumer_secret = 'SECRET'
access_token = 'TOKEN'
access_token_secret = 'TOKENSECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True)
search_words = "#மங்களஇசை_கேட்டநாள்"
date_since = "2021-08-05"
tweets = tweepy.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(100000)
print ("Tweepy Object",tweets)
date=[]
us=[]
o=0;
text=[]

for tweet in tweets:
    us.append(tweet)
    text.append(tweet.text)
    o+=1
# ~ print(o)

df=pd.DataFrame()

id=[]
for i in range(o):
    id.append(us[i]._json['id'])
date=[]
for i in range(o):
    date.append(us[i]._json['created_at'])
user=[]
for i in range(o):
    user.append(us[i]._json['user']['screen_name'])
text=[]
for i in range(o):
    text.append(us[i]._json['text'])

df['id']=id
df['date']=date
df['user']=user
df['text']=text


retweet=[]
for i in range(o):
    a=us[i]._json['text']
    if(a[0]=="R" and a[1]=="T"):
        retweet.append("True")
    else:
        retweet.append("False")
df['retweet']=retweet

retweet_count=[]
for i in range(o):
    retweet_count.append(us[i]._json['retweet_count'])
df["retweet_count"]=retweet_count

friends_count=[]
followers_count=[]
favourites_count=[]
location=[]
source=[]
for i in range(o):
    friends_count.append(us[i]._json['user']['friends_count'])
    followers_count.append(us[i]._json['user']['followers_count'])
    favourites_count.append(us[i]._json['user']['favourites_count'])
    location.append(us[i]._json['user']['location'])
    source.append(us[i]._json['source'][-11:-4])

df['location']=location
df['source']=source
df['followers_count']=followers_count
df['friends_count']=friends_count
df['favourite_count']=favourites_count

post_by=[]
for i in range(o):
    a=us[i]._json['entities']['user_mentions']
    #print(a)
    if(a):
        post_by.append(us[i]._json['entities']['user_mentions'][0]['screen_name'])
    else:
        post_by.append("null")
df['post_by']=post_by


print(df)
df.to_csv('tweets.csv')
