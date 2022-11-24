import json
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, url_contains

if __name__ == '__main__':
    # Load firefox and product page
    driver = webdriver.Firefox()
    with open('keys.json') as f:
        keys = json.load(f)
    print("Opening Firefox...")
    driver.get(keys['url'])
    while driver.find_element(By.CSS_SELECTOR, "[name='add']").get_attribute("disabled"):
        print('Still disabled, refreshing...')
        driver.refresh()
        time.sleep(0.5)

    # Select size
    select_box = driver.find_element(By.CSS_SELECTOR, "[name='options[Size]'")
    select = Select(select_box)
    select.select_by_value(keys['size'])

    # Add to cart and go to checkout
    driver.find_element(By.CSS_SELECTOR, "[name='add']").click()
    WebDriverWait(driver, 10).until(element_to_be_clickable((By.CSS_SELECTOR, "[action='/cart']"))).click()
    # driver.find_element(By.CSS_SELECTOR, "[action='/cart']").click()

    # Insert shipping information and move to billing
    WebDriverWait(driver, 7200).until(element_to_be_clickable((By.CSS_SELECTOR, "[name='email']"))).send_keys(keys['ship_email'])
    driver.find_element(By.CSS_SELECTOR, "[name='firstName']").send_keys(keys['ship_firstName'])
    driver.find_element(By.CSS_SELECTOR, "[name='lastName']").send_keys(keys['ship_lastName'])
    driver.find_element(By.CSS_SELECTOR, "[name='address1']").send_keys(keys['ship_address1'])
    driver.find_element(By.CSS_SELECTOR, "[name='address2']").send_keys(keys['ship_address2'])
    driver.find_element(By.CSS_SELECTOR, "[name='city']").send_keys(keys['ship_city'])
    driver.find_element(By.CSS_SELECTOR, "[name='zone']").send_keys(keys['ship_state'])
    driver.find_element(By.CSS_SELECTOR, "[name='postalCode']").send_keys(keys['ship_zip'])

    driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

    WebDriverWait(driver, 10).until(url_contains('shipping'))
    driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()

    # Insert billing information
    WebDriverWait(driver, 10).until(url_contains('payment'))
    driver.find_element(By.CSS_SELECTOR, "[for='billing_address_selector-custom_billing_address']").click()
    driver.find_element(By.CSS_SELECTOR, "[name='firstName']").send_keys(keys['bill_firstName'])
    driver.find_element(By.CSS_SELECTOR, "[name='lastName']").send_keys(keys['bill_lastName'])
    driver.find_element(By.CSS_SELECTOR, "[name='address1']").send_keys(keys['bill_address1'])
    driver.find_element(By.CSS_SELECTOR, "[name='address2']").send_keys(keys['bill_address2'])
    driver.find_element(By.CSS_SELECTOR, "[name='city']").send_keys(keys['bill_city'])
    driver.find_element(By.CSS_SELECTOR, "[name='zone']").send_keys(keys['bill_state'])
    driver.find_element(By.CSS_SELECTOR, "[name='postalCode']").send_keys(keys['bill_zip'])

    # Insert card information
    time.sleep(2)
    # driver.find_element(By.ID, "number").click()
    # driver.send_keys(keys['card_number'])
    # driver.find_element(By.ID, "name").send_keys(keys['card_name'])
    # driver.find_element(By.ID, "expiry").send_keys(keys['card_expiry'])
    # driver.find_element(By.ID, "verification_value").send_keys(keys['card_cvv'])

    exit()

    # Complete order
    print("Executing order...")
    driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
    print("Ordered!")