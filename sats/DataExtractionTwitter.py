import sys
import subprocess

import tweepy
import pandas as pd
import os

#from tkinter import *
#import tkinter.messagebox
#root=Tk()
#tkinter.messagebox.showinfo('Popup Window(Title)','This is a pop up window')
#root.mainloop()

os.remove('/home/sats/buttonpython/collected_tweets.txt') if os.path.exists('/home/sats/buttonpython/collected_tweets.txt') else None
os.remove('/home/sats/buttonpython/extracted_tweets.csv') if os.path.exists('/home/sats/buttonpython/extracted_tweets.csv') else None

#print("TweetId Extraction started")
a = sys.argv[1]

p1 = subprocess.Popen(['snscrape twitter-search " %s since:2020-01-01 until:2021-03-02 geocode:39.0119,-98.4842,2000km" > collected_tweets.txt' %(a)], shell = True)

try:
    p1.wait(timeout=300)
except subprocess.TimeoutExpired:
    p1.kill()


credentials_df = pd.read_csv('/home/sats/buttonpython/credentials.csv',header=None,names=['Name','Key'])
consumer_key = credentials_df.loc[credentials_df['Name']=='consumer_key','Key'].iloc[0]
consumer_secret = credentials_df.loc[credentials_df['Name']=='consumer_secret','Key'].iloc[0]
access_token = credentials_df.loc[credentials_df['Name']=='access_token','Key'].iloc[0]
access_token_secret = credentials_df.loc[credentials_df['Name']=='access_secret','Key'].iloc[0]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet_url = pd.read_csv("collected_tweets.txt", index_col= None, header = None, names = ["links"])

af = lambda x: x["links"].split("/")[-1]
tweet_url['ID'] = tweet_url.apply(af, axis=1)

idlist = tweet_url['ID'].tolist()
total_tweets = len(idlist)
batch = (total_tweets - 1) // 50 + 1
#print("TweetId Extraction finished")
#print(total_tweets)

def extract_tweets(tweet_ids):
    status = api.statuses_lookup(tweet_ids, tweet_mode= "extended")
    df = pd.DataFrame()
    for tweet in status:
        tweet_element = {"tweet_ID": tweet.id,
                         "username": tweet.user.screen_name,
                         "tweet": tweet.full_text,
                         "date": tweet.created_at,
                         "coordinates":tweet.coordinates,
                         "location": tweet.user.location,
                         "place": tweet.place}

        df = df.append(tweet_element, ignore_index=True)
    df.to_csv("extracted_tweets.csv", mode="a")

#print("Tweet Extraction started")

for i in range(batch):
        extract_batch = idlist[i*50:(i+1)*50]
        data = extract_tweets(extract_batch)

#print("Tweet Extraction finished")

#-----------------Sentiment Analysis ------------------------#

import pandas as pd
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob import Word


df1 = pd.read_csv('extracted_tweets.csv',lineterminator='\n')
df_total = pd.concat([df1])
Corpus = df_total.copy()

df_total['lowercase']=df_total['tweet'].apply(lambda x: " ".join(word.lower() for word in x.split()))
df_total['punctuation']=df_total['lowercase'].str.replace('[^\w\s]','')
stop_words=stopwords.words('english')

df_total['stopwords']=df_total['punctuation'].apply(lambda x: " ".join(word for word in x.split()if word not in stop_words))
df_total['lemmatize']=df_total['stopwords'].apply(lambda x:" ".join(Word(word).lemmatize() for word in x.split()))
df_total['polarity']=df_total['lemmatize'].apply(lambda x: TextBlob(x).sentiment[0])## just got polarity

from datetime import datetime, date
from wordcloud import WordCloud
all_words = ' '.join([text for text in df_total['lemmatize']])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.savefig("wordcloud.png")

tweetssorted = df_total.sort_values(by='polarity', ascending=True)
neg_tweets = tweetssorted[:10]
neg_tweets1 = neg_tweets['lemmatize']

tweetssorted = df_total.sort_values(by='polarity', ascending=False)
pos_tweets = tweetssorted[:10]
pos_tweets1 = pos_tweets['lemmatize']
pos_tweets2 = pos_tweets[['tweet_ID','tweet','username','lemmatize','polarity']].copy()

neg_tweets2 = neg_tweets[['tweet_ID','tweet','username','lemmatize','polarity']].copy()
pos_tweets2.insert(0, 'Sno', range(1, 1 + len(pos_tweets2)))
neg_tweets2.insert(0, 'Sno', range(1, 1 + len(neg_tweets2)))
#Sno_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
#df_sno = pd.DataFrame(Sno_list, columns=["Sno"])
#pos_tweets2["Sno"] = df_sno["Sno"]

neg_tweets2.to_csv("negtweets.csv")
pos_tweets2.to_csv("postweets.csv")

data = df_total.dropna()
pol = pd.DataFrame(columns = ['date','polarity','polarity2'])
pol['polarity'] = df_total['polarity']
pol['date'] = df_total['date']

for i in range(len(pol)):
    if pol.iloc[i, 1] >0:
        pol.iloc[i, 2] = "Positive"
    else:
        pol.iloc[i, 2] = "Negative"

pol['date'] = pd.to_datetime(pol['date'],errors='coerce')

pol['new_date'] = [datetime.date() for datetime in pol['date']]

pol2 = pol[['new_date', 'polarity2','polarity']].copy()
pol3 = pol2.groupby(['new_date','polarity2']).count()
pol3 = pol3.reset_index(drop=False)
pol3 = pol3.rename({'new_date': 'date', 'polarity2': 'polarity', 'polarity': 'count'}, axis='columns')
#pol3 = pol3.rename({'new_date': 'date', 'polarity2': 'polarity', 'polarity': 'num'}, axis='columns')
pol4 =pol3.pivot( index="date",columns="polarity", values="count")
pol4 = pol4.reset_index(drop=False)
pol4.insert(0, 'Sno', range(1, 1 + len(pol4)))


top20 = data['location'].value_counts()
top20 = top20[0:20]
top20 = top20.to_frame().reset_index()
top20.rename(columns = {'index':'location','location':'counts'}, inplace = True)
top20.insert(0, 'Sno', range(1, 1 + len(top20)))

top20.to_csv('top20locationtweeting.csv')
pol4.to_csv('polarity.csv')

#subprocess.call(['sh', '/home/sats/buttonpython/script.sh'])
#os.system("rm -r /home/sats/code/2")
#os.system("/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-pos.conf --config.reload.automatic --path.data /home/sats/code/2")
#os.system("rm -r /home/sats/code/2")
#os.system("/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-neg.conf --config.reload.automatic --path.data /home/sats/code/2")
#os.system("rm -r /home/sats/code/2")
#os.system("/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-pol.conf --config.reload.automatic --path.data /home/sats/code/2")
#os.system("rm -r /home/sats/code/2")
#os.system("/usr/share/logstash/bin/logstash -f /home/sats/buttonpython/logstash-t20.conf --config.reload.automatic --path.data /home/sats/code/2")

#os.system("scp -i keypair-django.pem postweets.csv ubuntu@ec2-3-137-213-13.us-east-2.compute.amazonaws.com:data/")
#os.system("scp -i keypair-django.pem negtweets.csv ubuntu@ec2-3-137-213-13.us-east-2.compute.amazonaws.com:data/")
#os.system("scp -i keypair-django.pem polarity.csv ubuntu@ec2-3-137-213-13.us-east-2.compute.amazonaws.com:data/")
#os.system("scp -i keypair-django.pem top20locationtweeting.csv ubuntu@ec2-3-137-213-13.us-east-2.compute.amazonaws.com:data/")
#os.system("scp -i keypair-django.pem wordcloud.png  ubuntu@ec2-3-133-149-6.us-east-2.compute.amazonaws.com:data/")
#
# sns.barplot(y="location", x="counts", data=top20)
# sns.set(rc={'figure.figsize':(15,10)})
# plt.savefig("locations_img.png")

#print("Sentiment Analysis Complete")
