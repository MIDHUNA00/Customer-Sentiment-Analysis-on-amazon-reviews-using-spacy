# We get started by importing spacy and pandas
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

# loading the taining data
df = pd.read_csv('https://raw.githubusercontent.com/MIDHUNA00/Customer-Sentiment-Analysis-on-amazon-reviews-using-spacy/main/reviewset1.csv')
df.head()

# droping null values
df.dropna(inplace = True)

# converting the float values in reviews to string
df['review_text'] = df['review_text'].astype('string')

# converting pandas dataframe column review_text to list
sentences = df.review_text.values.tolist()

# To get the target aspects and their sentiment descriptions
for sentence in sentences:
  doc = nlp(sentence)
  for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
      token.pos_,[child for child in token.children])

# Picking sentiment description using pos
for sentence in sentences:
  doc = nlp(sentence)
  descriptive_term = ''
  for token in doc:
    if token.pos_ == 'ADJ':
      descriptive_term = token
  print(sentence)
  print(descriptive_term)

# Picking up the intensifiers and adding them to their corresponding descriptive term
for sentence in sentences:
  doc = nlp(sentence)
  descriptive_term = ''
  for token in doc:
    if token.pos_ == 'ADJ':
      prepend = ''
      for child in token.children:
        if child.pos_ != 'ADV':
          continue
        prepend += child.text + ' '
      descriptive_term = prepend + token.text
  print(sentence)
  print(descriptive_term)

# Identifying the aspects
aspects = []
for sentence in sentences:
  doc = nlp(sentence)
  descriptive_term = ''
  target = ''
  for token in doc:
    if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
      target = token.text
    if token.pos_ == 'ADJ':
      prepend = ''
      for child in token.children:
        if child.pos_ != 'ADV':
          continue
        prepend += child.text + ' '
      descriptive_term = prepend + token.text
  aspects.append({'aspect': target,
    'description': descriptive_term})
print(aspects)

#calculating polarity and subjectivity of each aspects
from textblob import TextBlob
for aspect in aspects:
  aspect['sentiment'] = TextBlob(aspect['description']).sentiment
print(aspects)
