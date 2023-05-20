#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        csv_writer.writerow(['Review Title', 'Review Body', 'Review Rate', 'Review Date'])

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
product_url = input("Enter the URL of the Amazon product page: ")
num_pages = int(input("Enter the number of pages to scrape: "))

scrape_amazon_reviews(product_url, num_pages)


# In[ ]:




