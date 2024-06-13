# Approch

## Data Formatting and Storage:
Formatted the extracted data into JSON format. Stored the complete dataset as an NDJSON (Newline Delimited JSON) compressed file (ndjson.gz).

## Cookie Management:
Cookies are crucial for autofilling input fields on the website. Programmatically set cookies for the respective locations to simulate user input.

## Parallel Processing:
Used Python's multiprocessing module to handle restaurant data collection from multiple locations concurrently.

## Data Extraction Using Selenium:
Utilized Selenium WebDriver to automate browser interactions, including clicking and scrolling events, to ensure all data is loaded. Extracted necessary details using CSS selectors to pinpoint relevant HTML elements.

# Problem : 

## 1. Site Bloackage
Installed the System based VPN istead of Browser based VPN, as the brower window that is openned does not allow you to download VPN.

## 2. Selenium Chrome Webdriver
Got the diffuculty initially in setting up as the version didn't matched with the Broswer, after the Setup, sets the PATH environment variable.

## 3.Latitude and Longitude data was not visible in the HTML elements
Monitored network requests to identify the one returning geolocation data. Used URL https://portal.grab.com/foodweb/v2/merchants/{}?latlng=1.396364,103.747462 and replaced the restaurant_id dynamically to fetch latitude and longitude information from the response.

# Execution Steps:

Open cmd using Administrator and move to required folder

Install Required Packages:

Install dependencies listed in requirements.txt: pip install -r requirements.txt

Run the Program: python scraper.py
