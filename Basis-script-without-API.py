import tweepy
from collections import Counter
import re
from textblob import TextBlob
import nltk

# Authenticate with your Twitter Developer credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define a function to clean and tokenize text
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"@[^\s]+", "", text)  # Remove mentions
    text = re.sub(r"#", "", text)  # Remove hashtags
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    tokens = nltk.word_tokenize(text)  # Tokenize text
    return tokens

# Define a function to extract topics from tweets
def extract_topics(tweet_texts):
    topics = []
    for text in tweet_texts:
        # Clean and tokenize the text
        tokens = clean_text(text)
        
        # Use TextBlob to perform sentiment analysis and extract noun phrases
        blob = TextBlob(text)
        noun_phrases = blob.noun_phrases
        
        # Add the most common noun phrase to the list of topics
        if noun_phrases:
            topics.append(Counter(noun_phrases).most_common(1)[0][0])
        
        # Add the most common token to the list of topics if no noun phrases were found
        else:
            topics.append(Counter(tokens).most_common(1)[0][0])
    
    return topics

# Fetch 100 tweets containing the keyword "marketing"
tweets = api.search(q="marketing", count=100)

# Extract the text of each tweet
tweet_texts = [tweet.text for tweet in tweets]

# Extract the topics from the tweet texts
topics = extract_topics(tweet_texts)

# Print the most common topics
print("Top topics for keyword 'marketing':")
for topic, count in Counter(topics).most_common(10):
    print(f"{topic}: {count}")
