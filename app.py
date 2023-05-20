import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import spacy
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob

st.title("Amazon Review Scraper and Sentiment Analysis")
st.write("This website provides an inclusive overview of the product quality for any item available on Amazon.")

def scrape_amazon_reviews(product_url, num_pages):
    # Initialize the Chrome webdriver
    driver = webdriver.Chrome()

    # Navigate to the Amazon product page
    driver.get(product_url)

    # Click the "See all reviews" button
    see_all_reviews_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]'))
    )
    see_all_reviews_button.click()

    # Open a CSV file to write the scraped data
    with open('amazon_reviews.csv', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['review_title', 'review_text', 'Review Rate', 'Review Date'])

        # Loop through each page of reviews
        for _ in range(num_pages):
            # Get all the reviews on the current page
            reviews = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-hook="review"]'))
            )

            # Loop through each review and extract the data
            for review in reviews:
                title_element = review.find_elements(By.CSS_SELECTOR, 'a[data-hook="review-title"]')
                title = title_element[0].text if title_element else ''

                body_element = review.find_elements(By.CSS_SELECTOR, 'span[data-hook="review-body"]')
                body = body_element[0].text if body_element else ''

                rate_element = review.find_elements(By.CSS_SELECTOR, 'i[data-hook="review-star-rating"]')
                rate = rate_element[0].text if rate_element else ''

                date_element = review.find_elements(By.CSS_SELECTOR, 'span[data-hook="review-date"]')
                date = date_element[0].text if date_element else ''

                # Write the data to the CSV file
                csv_writer.writerow([title, body, rate, date])

            # Click the "Next" button to go to the next page of reviews
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a'))
            )
            next_button.click()

            # Wait for the next page of reviews to load
            time.sleep(2)

    # Close the CSV file and the Chrome webdriver
    driver.quit()

# Get the URL of the Amazon product page and the number of pages to scrape
product_url = st.text_input("Enter the URL of the Amazon product page: ")
num_pages = int(st.text_input("Enter the number of pages to scrape: "))

scrape_amazon_reviews(product_url, num_pages)


# Load Spacy's English language model
nlp = spacy.load('en_core_web_sm')

# Predefined aspects
nature_aspects = {
    "Phone and Appliances": ['Performance', 'Camera', 'Quality', 'Battery life', 'Sound'],
    "Costume and Fashion": ['Style and Design', 'Fit', 'Comfort', 'Fabric', 'Durability', 'Colour','Size']
}

# Read the customer review data into a pandas DataFrame
df = pd.read_csv("C:/Users/meenu/amazon_reviews.csv")
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
#print(doc_term_matrix)

nature = st.selectbox("Select the nature of the product", list(nature_aspects.keys()))
aspects = nature_aspects[nature]

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
#print(df['aspect'])

# Function to perform sentiment analysis on a review title or review body
def analyze_sentiment(review_title, review_text):
    sentence = review_title + ' ' + review_text
    blob = TextBlob(sentence)
    return blob.sentiment.polarity

# Get user input for the desired aspect

user_aspect = st.selectbox("Select your desired aspect",aspects)

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
#print(results_df)

# Calculate the average
# Calculate the average sentiment for the user's aspect
if 'sentiment' in results_df.columns:
    aspect_sentiment = results_df['sentiment'].mean()
else:
    aspect_sentiment = None

# Print the average sentiment for the user's aspect

if aspect_sentiment is not None:
    st.write(f"Average Sentiment: {aspect_sentiment}")
else:
    st.write("No sentiment data available for the user's aspect.")
