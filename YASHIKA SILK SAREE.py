
#Importing necessary libraries
import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the product page and the number of pages to scrape
URL = "https://www.amazon.in/Yashika-Womens-Blouse-Sdpl-Swati-Navy_Multicolor/product-reviews/B07HL695YR/ref=cm_cr_dp_d_show_all_btm?ie=UT"


pages = 10

# Create a CSV file to store the data
with open('reviewset4.csv', 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['review_title', 'review_text', 'review_rating'])

    # Scrape the reviews from each page
    for i in range(1, pages + 1):
        # Send the HTTP request and parse the response
        res = requests.get(URL + '&pageNumber=' + str(i))
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract the review title, text, rating, and date
        review_titles = soup.find_all('a', {'data-hook': 'review-title'})
        review_texts = soup.find_all('span', {'data-hook': 'review-body'})
        review_ratings = soup.find_all('i', {'data-hook': 'review-star-rating'})

        # Write the data to the CSV file
        for j in range(len(review_titles)):
            writer.writerow([review_titles[j].text, review_texts[j].text, review_ratings[j].text])

import pandas as pd
data = pd.read_csv('reviewset4.csv')
print(data)
print(data.head(5))