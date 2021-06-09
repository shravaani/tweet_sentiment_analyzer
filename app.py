
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns



consumerKey = "gKuDU5lm0yQpSzTAmhaC4Pqr6"
consumerSecret = "53OkakYGPvLCTOC9CC0LAmLdV0IVucBEOe5JT8S8otmDSEINSC"
accessToken = "1355811610305040386-1QOfrs6CnEqgHR7iAtVNtjrOTBiNhy"
accessTokenSecret = "ofK0tHyaVRkFw8iFWpRIrkglbfvDReJPFHtEigBbPg8yl"


#Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
    
# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret) 
    
# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True)



#plt.style.use('fivethirtyeight')

# tweepy comes with limitations of 198 tweets
 
def app():


	st.title("Twitter Sentiment Analyzer")


	activities=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Activity",activities)

	

	if choice=="Tweet Analyzer":

		st.subheader("Analyze the tweets of your favourite Personalities")

		# st.subheader("Tweepy comes with limitation of 198 while usig streamlit")

		st.write('Analysize and Visualize the Tweets ')


		raw_text = st.text_area("Enter twitter Handler name without @")
		#tweets_count = st.text_input("Enter teh count of tweets")
		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Visualize the Sentiment Analysis"])


		if st.button("Analyze"):

			
			if Analyzer_choice == "Show Recent Tweets":

				st.success("Fetching last Tweets")  # fetching last 2o tweets

				
				def Show_Recent_Tweets(raw_text):

					# Extract 100 tweets from the twitter user
					posts = api.user_timeline(screen_name=raw_text, count = 198, lang ="en", tweet_mode="extended")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:50]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			else:
	
				def Plot_Analysis():

					st.success("Generating Bar Graph for Sentiment Analysis")

					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					# Create a function to clean the tweets
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
					 text = re.sub('#', '', text) # Removing '#' hash tag
					 text = re.sub('RT[\s]+', '', text) # Removing RT
					 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
					 
					 return text


					# Clean the tweets
					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity

					# Create a function to get the polarity
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)


					def getAnalysis(score):
					  if score < 0:
					    return 'Negative'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))


				st.pyplot(use_container_width=True)

				

	

	else:

		st.subheader("fetches the last tweets from the twitter handel")

		
		st.write("1. Analyzes Polarity of tweets and adds an additional column for it")
		st.write("2. Analyzes Sentiments of tweets and adds an additional column for it")






		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")
		# tweet_counts = st.text_input('Enter the count of tweets')
		# print(tweet_counts)
		
		def get_data(user_name):

			posts = api.user_timeline(screen_name=user_name, count = 198, lang ="en", tweet_mode="extended")

			df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

			def cleanTxt(text):
				text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
				text = re.sub('#', '', text) # Removing '#' hash tag
				text = re.sub('RT[\s]+', '', text) # Removing RT
				text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
				return text

			# Clean the tweets
			df['Tweets'] = df['Tweets'].apply(cleanTxt)


			def getSubjectivity(text):
				return TextBlob(text).sentiment.subjectivity

						# Create a function to get the polarity
			def getPolarity(text):
				return  TextBlob(text).sentiment.polarity


						# Create two new columns 'Subjectivity' & 'Polarity'
			df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
			df['Polarity'] = df['Tweets'].apply(getPolarity)

			def getAnalysis(score):
				if score < 0:
					return 'Negative'

				elif score == 0:
					return 'Neutral'


				else:
					return 'Positive'

		
						    
			df['Analysis'] = df['Polarity'].apply(getAnalysis)
			return df

		if st.button("Show Data"):

			st.success("Fetching Last Tweets")

			df=get_data(user_name)

			st.write(df)



			

				


























if __name__ == "__main__":
	app()