# Day53-Capstone-webscrape
Zillow Property Scraper

This repository contains a Python script that scrapes rental property listings from Zillow and submits the data to a Google Sheets form.
Features

    Scrapes rental property listings from Zillow using Beautiful Soup.
    Extracts property address, price, and listing URL.
    Submits the scraped data to a Google Sheets form using Selenium.

Dependencies

    Python 3
    Selenium
    Beautiful Soup 4

Usage

    Clone this repository:

bash

git clone https://github.com/your-github-username/your-repo-name.git

    Install the required packages:

pip install -r requirements.txt

    Update the GOOGLE_SHEET and HEMNET variables with your own Google Sheets form URL and Zillow search URL, respectively.

    Run the script:

python zillow_scraper.py

This will launch a Firefox browser window, scrape the rental property data from Zillow, and submit the data to the Google Sheets form.
Notes

    Ensure that you have the Firefox WebDriver (geckodriver) installed and added to your system's PATH.
    The script might need to be adjusted depending on the structure of your Google Sheets form.
    The User-Agent header might need to be updated to avoid potential request blocks from Zillow.
