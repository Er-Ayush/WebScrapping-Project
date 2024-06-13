import time
import os
import multiprocessing
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

import json
import gzip

import requests

def scrape_restaurants(driver, browser_cookies):

    restaurant_info = []
    driver.get('https://food.grab.com/sg/en/')  
    time.sleep(2)

    for key, val in browser_cookies.items():
        driver.add_cookie({"name": key, "value": val})
    time.sleep(2)

    driver.refresh() 

    search_btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[3]/div[3]/div/button")))
    search_btn.click()

    time.sleep(10)

    element_count = 0   

    for i in range(20): 

        restaurant_elements = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.RestaurantListCol___1FZ8V")))

        last_element = restaurant_elements[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_element)
        time.sleep(5)

        for restaurant in restaurant_elements[element_count:]:
            element_count += 1
            try:
                cuisine_type = restaurant.find_element(By.CSS_SELECTOR, "div.basicInfoRow___UZM8d").text
                restaurant_name = restaurant.find_element(By.CSS_SELECTOR, "p.name___2epcT").text
                rating_value = restaurant.find_element(By.CSS_SELECTOR, "div.numbersChild___2qKMV:nth-child(1)").text
                duration_dist = restaurant.find_element(By.CSS_SELECTOR, "div.numbersChild___2qKMV:nth-child(2)").text
                image_elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.show___3oA6B")))
                image_src = image_elem.get_attribute("src")
                restaurant_id = restaurant.find_element(By.CSS_SELECTOR, "a").get_attribute("href").split('/')[-1][:-1]

                api_url = f"https://portal.grab.com/foodweb/v2/merchants/{restaurant_id}?latlng=1.396364,103.747462"
                api_response = requests.get(api_url)

                if api_response.status_code == 200:
                    data = json.loads(api_response.text)
                    latitude = data['merchant']['latlng']['latitude']
                    longitude = data['merchant']['latlng']['longitude']
                    eta_value = data['merchant']['ETA']
                    delivery_fee = data['merchant']['estimatedDeliveryFee']
                else:
                    latitude = "N/A"
                    longitude = "N/A"

                try:
                    promo_elem = restaurant.find_element(By.CSS_SELECTOR, "p.promoText___2LmzI")
                    promo_available = "True"
                except NoSuchElementException:
                    promo_available = "False"

                try:
                    discount_elem = restaurant.find_element(By.CSS_SELECTOR, "span.discountText___GQCkj")
                    discount_info = discount_elem.text
                except NoSuchElementException:
                    discount_info = "No discount"

                try:
                    notice_elem = restaurant.find_element(By.CSS_SELECTOR, "p.closeSoon___1eGf8")
                    promo_notice = notice_elem.text
                except NoSuchElementException:
                    promo_notice = "No promo"

                restaurant_dict = {
                    "Restaurant Id": restaurant_id,
                    "Restaurant Name": restaurant_name,
                    "Cuisine": cuisine_type,
                    "Rating": rating_value,
                    "Duration": duration_dist,
                    "Promo": promo_available,
                    "Offers": discount_info,
                    "Notice": promo_notice,
                    "Image URL": image_src,
                    "Latitude": latitude,
                    "Longitude": longitude,
                    "ETA": eta_value,
                    "Estimated Delivery Fee": delivery_fee
                }

                restaurant_info.append(restaurant_dict)

            except NoSuchElementException:
                continue

    with gzip.open(f"restaurant_data_{multiprocessing.current_process().name}.ndjson.gz", "wt", encoding="utf-8") as f:
        for data in restaurant_info:
            json.dump(data, f)
            f.write('\n')

    time.sleep(20)

def run_scraping(browser_cookies):

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(service=service, options=options)
    
    scrape_restaurants(driver, browser_cookies)

    driver.quit()

def initialize_process():

    cookies_set = [{
        "gfc_country": "SG",
        "gfc_session_guid": "694226c1-b9c1-4b47-89a7-0d98fc4abe21",
        "next-i18next": "en",
        "_gsvid": "1a6fec89-c5b1-421e-a7cb-21586fcb3a1e",
        "_gcl_au": "1.1.701740744.1715357490",
        "hwuuid": "adc3d9c5-d28c-4470-8cd5-1d400945a0ff",
        "hwuuidtime": "1715357540",
        "_ga": "GA1.1.1032334565.1715454609",
        "location": '{"latitude":1.367476,"longitude":103.858326,"address":"Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456","countryCode":"SG","isAccurate":true,"addressDetail":"Chong Boon Dental Surgery - Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456","noteToDriver":"","city":"Singapore City","cityID":6,"displayAddress":"Chong Boon Dental Surgery - Block 456 Ang Mo Kio Avenue 10, #01-1574, Singapore, 560456"}',
        "pid": "www.google.com",
        "c": "non-paid",
        "_gssid": "2404151150-xial46y7nxr",
        "_ga_RPEHNJMMEM": "GS1.1.1715773927.6.0.1715773927.60.0.995007504"
    },
    {
        "gfc_country": "SG",
        "gfc_session_guid": "694226c1-b9c1-4b47-89a7-0d98fc4abe21",
        "next-i18next": "en",
        "_gsvid": "1a6fec89-c5b1-421e-a7cb-21586fcb3a1e",
        "_gcl_au": "1.1.701740744.1715357490",
        "hwuuid": "adc3d9c5-d28c-4470-8cd5-1d400945a0ff",
        "hwuuidtime": "1715357540",
        "_ga": "GA1.1.1032334565.1715454609",
        "location": '{"latitude": 1.396364,"longitude": 103.747462,"address": "Choa Chu Kang North 6, Singapore, 689577","countryCode": "SG", "isAccurate": true, "addressDetail": "PT Singapore - Choa Chu Kang North 6, Singapore, 689577", "noteToDriver": "", "city": "Singapore City", "cityID": 6, "displayAddress": "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"}',
        "pid": "www.google.com",
        "c": "non-paid",
        "_gssid": "2404151909-niaypmwmt29",
        "_ga_RPEHNJMMEM": "GS1.1.1715800156.7.1.1715800314.54.0.1428779389"
    }]
    processes = []
    for idx, cookies in enumerate(cookies_set, start=1):
        process = multiprocessing.Process(
            target=run_scraping, args=(cookies,), name=f"Process-{idx}")
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    TIMEOUT = 600
    initialize_process()
