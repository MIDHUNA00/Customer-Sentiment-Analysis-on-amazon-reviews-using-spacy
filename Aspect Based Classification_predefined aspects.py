#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
from spacy.lang.en import English
from spacy import displacy
from spacy.util import minibatch, compounding
import pandas as pd
import numpy as np
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob

# Load Spacy's English language model
nlp = spacy.load('en_core_web_sm')

# Load the Amazon review dataset
df = pd.read_csv('https://raw.githubusercontent.com/MIDHUNA00/Customer-Sentiment-Analysis-on-amazon-reviews-using-spacy/main/reviewset4.csv')


# Check for missing values and replace with empty string
df['review_text'] = df['review_text'].fillna('')

# Preprocess the text data
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuations and digits
    text = re.sub('[%s]' % re.escape(string.punctuation + string.digits), '', text)
    # Remove stop words
    stop_words = stopwords.words('english')
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Apply the preprocessing function to the review text column
df['review_text'] = df['review_text'].apply(preprocess_text)

# Create a document-term matrix using CountVectorizer
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
doc_term_matrix = vectorizer.fit_transform(df['review_text'])

# Define the number of topics to identify
num_topics = 5

# Apply Latent Dirichlet Allocation to identify the topics
lda_model = LatentDirichletAllocation(n_components=num_topics, max_iter=10, learning_method='online')
lda_model.fit(doc_term_matrix)

# Print the topics and their top words
def print_topics(model, vectorizer, n_top_words):
    words = vectorizer.get_feature_names()
    for i, topic in enumerate(model.components_):
        print("Topic %d:" % (i))
        print(" ".join([words[j] for j in topic.argsort()[:-n_top_words - 1:-1]]))

print_topics(lda_model, vectorizer, 10)

# Map the topics to aspects
aspects = {
    0: 'price',
    1: 'quality',
    2: 'usability',
    3: 'design',
    4: 'performance'
}

# Classify the reviews based on their aspect
def classify_review(review_text):
    # Apply Spacy's English language model to the review text
    doc = nlp(review_text)
    # Identify the topic distribution of the review text using the trained LDA model
    topic_dist = lda_model.transform(vectorizer.transform([review_text]))
    # Map the most likely topic to an aspect
    aspect = aspects[np.argmax(topic_dist)]
    return aspect

# Apply the classify_review function to the review text column
df['aspect'] = df['review_text'].apply(classify_review)

# Apply sentiment analysis on the review text for each aspect separately
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

for aspect in aspects.values():
    aspect_df = df[df['aspect'] == aspect]
    aspect_df = aspect_df.assign(sentiment=aspect_df['review_text'].apply(analyze_sentiment))
    print(f"Aspect: {aspect}")
    print(f"Average Sentiment: {aspect_df['sentiment'].mean()}")
    


# In[ ]:




