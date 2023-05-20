#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import spacy
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob

# Load Spacy's English language model
nlp = spacy.load('en_core_web_sm')

# Predefined aspects
aspects = {
    'Style and design',
    'Fit and comfort',
    'Fabric quality',
    'Durability',
    'Color options',
    'Size range',
    'Price',
    'Brand reputation',
    'Washing and care instructions'
}

# Read the customer review data into a pandas DataFrame
df = pd.read_csv('https://raw.githubusercontent.com/MIDHUNA00/Customer-Sentiment-Analysis-on-amazon-reviews-using-spacy/main/reviewset4.csv')

# Preprocess the text data
def preprocess_text(text):
    if isinstance(text, str):  # Check if text is a valid string
        # Convert to lowercase
        text = text.lower()
        # Remove punctuations and digits
        text = re.sub('[%s]' % re.escape(string.punctuation + string.digits), '', text)
        # Remove stop words
        stop_words = stopwords.words('english')
        text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Apply preprocessing to the review text column
df['review_text'] = df['review_text'].apply(preprocess_text)

# Create a document-term matrix using CountVectorizer
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
doc_term_matrix = vectorizer.fit_transform(df['review_text'])

# Define the number of topics to identify
num_topics = len(aspects)

# Apply Latent Dirichlet Allocation to identify the topics
lda_model = LatentDirichletAllocation(n_components=num_topics, max_iter=10, learning_method='online')
lda_model.fit(doc_term_matrix)

# Map the topics to aspects
topic_aspects = dict(enumerate(aspects))

# Function to classify the review aspect based on the LDA model
def classify_aspect(review_text):
    # Apply Spacy's English language model to the review text
    doc = nlp(review_text)
    # Identify the topic distribution of the review text using the trained LDA model
    topic_dist = lda_model.transform(vectorizer.transform([review_text]))
    # Map the most likely topic to an aspect
    aspect_topic = topic_dist.argmax()
    return topic_aspects[aspect_topic]

# Apply the classify_aspect function to the review text column
df['aspect'] = df['review_text'].apply(classify_aspect)

# Function to perform sentiment analysis on a review title or review body
def analyze_sentiment(review_title, review_text):
    sentence = review_title + ' ' + review_text
    blob = TextBlob(sentence)
    return blob.sentiment.polarity

# Get user input for the desired aspect
user_aspect = input("Enter your desired aspect: ")

# Perform aspect-based sentiment analysis on the customer reviews
results = []

for index, row in df.iterrows():
    review_title = preprocess_text(row['review_title'])
    review_text = preprocess_text(row['review_text'])
    aspect = row['aspect']
    if aspect == user_aspect:
        sentiment = analyze_sentiment(review_title, review_text)
        results.append({'aspect': aspect, 'review_title': review_title, 'review_text': review_text, 'sentiment': sentiment})

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Calculate the average
# Calculate the average sentiment for the user's aspect
if 'sentiment' in results_df.columns:
    aspect_sentiment = results_df['sentiment'].mean()
else:
    aspect_sentiment = None

# Print the average sentiment for the user's aspect
print(f"Aspect: {user_aspect}")
if aspect_sentiment is not None:
    print(f"Average Sentiment: {aspect_sentiment}")
else:
    print("No sentiment data available for the user's aspect.")


# In[ ]:




