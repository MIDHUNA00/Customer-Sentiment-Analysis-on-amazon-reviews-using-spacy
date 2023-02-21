#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/MIDHUNA00/Customer-Sentiment-Analysis-on-amazon-reviews-using-spacy/main/reviewset1.csv')


# In[2]:


df.dropna(inplace = True)
df['review_title'] = df['review_title'].astype('string')
df['review_text'] = df['review_text'].astype('string')


# In[3]:


df.head()


# In[4]:


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

nlp = spacy.load("en_core_web_sm")

def preprocess_reviews(reviews):
    # Remove whitespace
    reviews = reviews.str.strip()

    # Replace non-alphabetic characters with spaces
    reviews = reviews.str.replace(r'[^a-zA-Z\s]', ' ')

    # Convert to lowercase
    reviews = reviews.str.lower()

    # Tokenize using Spacy
    reviews = reviews.apply(lambda x: nlp(x))

    # Remove stopwords and punctuation
    reviews = reviews.apply(lambda x: [token.lemma_ for token in x if not token.is_stop and not token.is_punct])

    # Join tokens back into strings
    reviews = reviews.apply(lambda x: ' '.join(x))

    return reviews

def topic_detection(reviews, n_topics):
    # Preprocess the reviews
    preprocessed_reviews = preprocess_reviews(reviews)

    # Vectorize the reviews using a bag-of-words model
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(preprocessed_reviews)

    # Perform LDA topic modeling
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
    lda.fit(vectors)

    # Print the top words for each topic
    feature_names = vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(lda.components_):
        top_features = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        print("Topic %d: %s" % (topic_idx, ", ".join(top_features)))


# In[8]:


# Example usage

reviews = df['review_text']

topic_detection(reviews, n_topics=5)


# In[ ]:





# In[ ]:




