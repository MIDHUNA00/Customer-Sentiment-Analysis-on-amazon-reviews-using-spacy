#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import csv
from selenium import webdriver

# Get the URL of the Amazon product page and the number of pages to scrape
product_url = input("Enter the URL of the Amazon product page: ")
num_pages = int(input("Enter the number of pages to scrape: "))

# Initialize the Chrome webdriver
driver = webdriver.Chrome()

# Navigate to the Amazon product page
driver.get(product_url)

# Click the "See all reviews" button
see_all_reviews_button = driver.find_elements("xpath",'//a[@data-hook="see-all-reviews-link-foot"]')[0]
see_all_reviews_button.click()

# Wait for the reviews page to load
time.sleep(2)

# Open a CSV file to write the scraped data
csv_file = open('amazon_reviews.csv', 'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Review Title', 'Review Body', 'Review Rate', 'Review Date'])

# Loop through each page of reviews
for i in range(num_pages):

    # Get all the reviews on the current page
    reviews = driver.find_elements("xpath",'//div[@data-hook="review"]')
    
    # Loop through each review and extract the data
    for review in reviews:
        title_element = review.find_elements("xpath",'.//a[@data-hook="review-title"]')
        if title_element:
            title = title_element[0].text
        else:
            title = ''
        
        body_element = review.find_elements("xpath",'.//span[@data-hook="review-body"]')
        if body_element:
            body = body_element[0].text
        else:
            body = ''
        
        rate_element = review.find_elements("xpath",'.//i[@data-hook="review-star-rating"]')
        if rate_element:
            rate = rate_element[0].text
        else:
            rate = ''
        
        date_element = review.find_elements("xpath",'.//span[@data-hook="review-date"]')
        if date_element:
            date = date_element[0].text
        else:
            date = ''
        
        # Write the data to the CSV file
        csv_writer.writerow([title, body, rate, date])

    # Click the "Next" button to go to the next page of reviews
    next_button = driver.find_elements("xpath",'//li[@class="a-last"]//a')
    if next_button:
        next_button[0].click()
    else:
        break

    # Wait for the next page of reviews to load
    time.sleep(2)

# Close the CSV file and the Chrome webdriver
csv_file.close()
driver.quit()


# In[2]:


import pandas as pd
data = pd.read_csv('amazon_reviews.csv')
data.info()


# In[ ]:




