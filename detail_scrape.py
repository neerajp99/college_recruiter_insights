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
	driver.maximize_window()
	driver.get(target_url)
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "header__content__heading")))
	print(element)
	return driver
# Method to log in into Linkedin account
def linkedin_login(driver):
	"""
		Find the input fields, add credentials and click log in
	"""
	email_field = driver.find_element_by_id('username').send_keys("email")
	password_field = driver.find_element_by_id('password').send_keys("password")
	login_button = driver.find_element_by_class_name('btn__primary--large').click()

	# Update the driver 
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-global-typeahead__input")))
	print(element)

"""
	Redirect to school alumni page, scraps all the data of alumni
"""
def get_school_data(driver, school_link):
	# Navigate to the specific school url
	driver.get(school_link)

	headings = ["Where they live", "Where they work", "What they do", "What they studied", "What they are skilled at"]


	# Dictionary to contain data
	data = dict()	

	# Click view more to change classes 
	time.sleep(2)
	driver.find_element_by_class_name('org-people__show-more-button').click()
	time.sleep(2)

	# New counter variables 
	table_counter = 0
	list_counter = 0
	while(table_counter < 5):
		# time.sleep(3)
		# for i in range(table_counter // 2):
		# 	driver.find_element_by_class_name('artdeco-pagination__button--next').click()
		# 	time.sleep(5)

		# Add the click table heading as the key to the data dictionary
		data[headings[table_counter]] = {}
		
		# Loop over the 15 
		while( list_counter < 15):
			time.sleep(2)
			for i in range(table_counter // 2):
				driver.find_element_by_class_name('artdeco-pagination__button--next').click()
				time.sleep(2)

			time.sleep(1)
			# Count the number of elements inside a table
			# count_tables_container = driver.find_elements_by_class_name("artdeco-carousel__item-container")[table_counter]
			# number_of_elements = len(count_tables_container.find_elements_by_class_name('org-people-bar-graph-element--is-selectable'))
			print('COUNNNNNNNNNNT')

			# try:
			# 	# Press the show more button to change class
			# 	driver.find_element_by_class_name('org-people__show-more-button').click()
			# except: 
			# 	pass

			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "artdeco-carousel__item-container")))
			details = driver.find_elements_by_class_name('artdeco-carousel__item-container')[table_counter]
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "org-people-bar-graph-element--is-selectable")))
			detail = details.find_elements_by_class_name('org-people-bar-graph-element--is-selectable')[list_counter]
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "org-people-bar-graph-element__category")))
			detail_string = detail.find_element_by_class_name('org-people-bar-graph-element__category').text
			
			time.sleep(3)

			# Initialise the key of each place as an empty object
			data[headings[table_counter]][detail_string] = {}
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "org-people-bar-graph-element__category")))
			detail_link = detail.find_element_by_class_name('org-people-bar-graph-element__category')
			
			detail_link.click()
			time.sleep(3)
			# try:
			# 	# Press the show more button to change class
			# 	driver.find_element_by_class_name('org-people__show-more-button').click()
			# except: 
			# 	pass
			print("Clicked!")

			# Extract other tables for the specific click 
			temp = table_counter;

			# Counter to keep a check of number of tables explored
			inner_table_counter = -1

			# Counter for incrementing xpath values 
			xpath_counter = 0

			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "artdeco-button--tertiary")))
				
			# Loop over all the tables 
			for content in driver.find_elements_by_class_name('artdeco-carousel__item-container'):
				xpath_counter += 1
				inner_table_counter += 1
				# time.sleep(3)
				print('1')
				# Restricting the program to run for just 5 times
				if inner_table_counter < 5:
					print('2')
					# Skip the table whose item is clicked
					if inner_table_counter != table_counter:
						print('3')
						# Initialise each value's key as the heading of the table
						data[headings[table_counter]][detail_string][headings[inner_table_counter]] = {}

						# Starting counter value for list index of <strong> attribute
						strong_counter = 2
						print('4')

						WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "org-people-bar-graph-element--is-selectable")))
							

						# Loop over each item in the table and add it to the table 
						for inner_content in content.find_elements_by_class_name('org-people-bar-graph-element--is-selectable'):
							print('5')
							# Copy the label
							label = inner_content.find_element_by_class_name('org-people-bar-graph-element__category').text 
							print("LABEL", label)
							# Copy the label value 
							# time.sleep(2)
							print(xpath_counter, strong_counter, table_counter, list_counter)
							# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "org-people-bar-graph-element__percentage-bar-info")))
							# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/ul/li[" + str(xpath_counter) + "]/div/div/div/div[" + str(strong_counter) + "]/div/strong")))
							# label_value = inner_content.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/ul/li[" + str(xpath_counter) + "]/div/div/div/div[" + str(strong_counter) + "]/div/strong").text
							while (True):
								try:
									label_value = inner_content.find_element_by_xpath("/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/ul/li[" + str(xpath_counter) + "]/div/div/div/div[" + str(strong_counter) + "]/div/strong").text
									# label_value = inner_content.driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/section/div[2]/ul/li[" + str(xpath_counter) + "]/div/div/div/div[" + str(strong_counter) + "]/div/strong").text
									break
								except:
									label_value = 1000000000000000000000000000000000001
									break
							# Add the label and label value to the data as key value pair 
							data[headings[table_counter]][detail_string][headings[inner_table_counter]][label] = label_value 

							# Increment the <strong> counter 
							strong_counter += 1 
							print('6')
				# Click the next slide button after every 2 tables 
				if xpath_counter % 2 == 0 and xpath_counter < 6:
					print('7')
					time.sleep(2)
					WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-pagination__button--next')))
					driver.find_element_by_class_name('artdeco-pagination__button--next').click()
					time.sleep(1)
				# Increment the inner table counter 
				# inner_table_counter += 1
				# xpath_counter += 1
				print('8')
			#Collect tables
			print('9')
			driver.get(school_link)
			time.sleep(4)
			try:
				# Press the show more button to change class
				driver.find_element_by_class_name('org-people__show-more-button').click()
			except: 
				pass
			list_counter += 1
		table_counter += 1
		list_counter = 0

		print('10')	
	return data


if __name__ == '__main__':
	try: 
		# Add the initial target url
		target_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
		driver = configure_webDriver(target_url)
		# Call the function to login into Linkedin account
		linkedin_login(driver)
		school_link = "https://www.linkedin.com/school/california-institute-of-technology/people/"
		final_school_data = get_school_data(driver, school_link)
		# Dumps the data 
		final_school_data = json.dumps(final_school_data, indent = 4)
		# Store the values into a .json file
		with open('caltech.json', 'w') as f:
			f.write(final_school_data)

		
		# for i in range(5):
		# 	final_school_data = get_school_data(driver, school_link, i)
		# 	# Dumps the data 
		# 	final_school_data = json.dumps(final_school_data, indent = 4)
		# 	# Store the values into a .json file
		# 	with open('mit.json' + str(i), 'w') as f:
		# 		f.write(final_school_data)
	except Exception as e:
		print(e)
	finally: 
		driver.quit()