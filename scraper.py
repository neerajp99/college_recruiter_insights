import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome 
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import string


# Configure and prepare the webdriver
def configure_webDriver(target_url):
	driver = webdriver.Firefox()
	driver.get(target_url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "header__content__heading")))
	print(element)
	return driver

# Method to log in into Linkedin account
def linkedin_login(driver):
	"""
		Find the input fields, add credentials and click log in
	"""
	email_field = driver.find_element_by_id('username').send_keys("YOUR_EMAIL-ID")
	password_field = driver.find_element_by_id('password').send_keys("YOUR_PASSWORD")
	login_button = driver.find_element_by_class_name('btn__primary--large').click()

	# Update the driver 
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))
	print(element)

"""
	Redirect to school alumni page, scraps all the data of alumni
"""
def get_school_data(driver):
	# Navigate to the specific school url
	driver.get('https://www.linkedin.com/school/harvard-university/people/')

	headings = ["Where they live", "Where they work", "What they do", "What they studied", "What they are skilled at"]

	counter = 0

	# Dictionary to contain data
	data = dict()

	# Keep a counter to check when to click the next page button
	list_counter = 1

	# Click view more to change classes 
	time.sleep(3)
	driver.find_element_by_class_name('org-people__show-more-button').click()
	time.sleep(3)

	# Loop over the list items to get the information
	for content in driver.find_elements_by_class_name('artdeco-carousel__item-container'):
		
		
		# Let the program run for just 5 times
		if counter < 5:
			# Add heading item as a the key and empty object as the value 
			data[headings[counter]] = {}

			# Starting counter value for list index of <strong> attribute
			strong_counter = 2

			# Loop over each list item
			for live in content.find_elements_by_class_name('org-people-bar-graph-element--is-selectable'):
				content_string = live.find_element_by_class_name('org-people-bar-graph-element__category').text
				content_integer = live.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/ul/li[" + str(list_counter) + "]/div/div/div/div[" + str(strong_counter) + "]/div/strong").text	
					
				# Store the data values 
				data[headings[counter]][content_string] = content_integer

				# Increment the <strong> counter
				strong_counter += 1
        # Click the next page button after every 2 tables
		if list_counter % 2 == 0:
			driver.find_element_by_class_name('artdeco-pagination__button--next').click()
			time.sleep(5)
		# Increment the counters
		list_counter += 1
		counter += 1		
	return data
if __name__ == '__main__':
	try: 
		# Add the initial target url
		target_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
		driver = configure_webDriver(target_url)
		# Call the function to login into Linkedin account
		linkedin_login(driver)
		final_school_data = get_school_data(driver)
		# Dumps the data 
		final_school_data = json.dumps(final_school_data, indent = 4)
		# Store the values into a .json file
		with open('harvard.json', 'w') as f:
			f.write(final_school_data)
	finally: 
		driver.quit()




