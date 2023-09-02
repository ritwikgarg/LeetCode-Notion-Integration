import requests
import sys
import os
import time
import json
from decouple import config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Read sensitive information from environment variables or a .env file
notion_key = config('notion_key')
database_id = config('database_id')

# Function to open a headless Chrome browser
def openBrowser(url):
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # Create a new headless Chrome browser instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the specified URL and maximize the window
    driver.get(url)
    driver.maximize_window()
    return driver

# Function to close the browser
def closeBrowser(driver):
    driver.close()

# Function to fetch data from a LeetCode page
def fetchPageData(pageUrl):
    sleepTime = 3

    # Open a headless Chrome browser
    browser = openBrowser(pageUrl)
    time.sleep(sleepTime)
    pageSource = browser.page_source

    # Wait for the LeetCode page to load completely
    WebDriverWait(browser, 10).until(EC.title_contains("LeetCode"))

    # Create a BeautifulSoup object for parsing the HTML
    newSoup = BeautifulSoup(pageSource, 'html.parser')

    # Check if the page is a valid LeetCode question page
    if (browser.title.endswith("LeetCode")):
        print("\n\n------------------- Parsing data -------------------\n\n")

        # Extract question name and ID
        question_name_and_id = newSoup.find("div", class_="flex h-full items-center").find("a")
        question = question_name_and_id.text.split('.')
        question_id = question[0]
        question_title = question[1].strip()
        print(f"Question Id: {question_id}")
        print(f"Question Title: {question_title}")

        # Extract tags
        tags_parent_div = newSoup.find("div", class_="mt-2 flex flex-wrap gap-y-3")
        a_elements = tags_parent_div.find_all("a")
        tags = [a.text.strip() for a in a_elements]
        print(f"Tags: {tags}")

        # Extract difficulty
        count = 0
        difficulty = None
        while difficulty is None:
            if(count == 0):
                difficulty = newSoup.find("div", class_= "text-olive dark:text-dark-olive inline-block text-sm font-medium capitalize leading-[22px]")
            if(count == 1):
                difficulty = newSoup.find("div", class_= "text-yellow dark:text-dark-yellow inline-block text-sm font-medium capitalize leading-[22px]")
            if(count == 2):
                difficulty = newSoup.find("div", class_= "text-pink dark:text-dark-pink inline-block text-sm font-medium capitalize leading-[22px]")
            count += 1
        print(f"Difficulty: {difficulty.text}")
        print("\n\n------------------- Done -------------------\n\n")

        # Close the browser
        closeBrowser(browser)

    else:
        print("Page does not exist or connection failed, status code:", newSoup.status_code)

    return question_id, question_title, tags, difficulty.text

# Function to create properties data for adding to the Notion database
def create_properties_data(leetcode_URL, question_id, tags, difficulty, question_title):
    properties = {
        "properties":
        {
            "Question": {
                "url": leetcode_URL
            },
            "Id": {
                "number": int(question_id)
            },
            "Category": {
                "multi_select": [{"name": tag} for tag in tags]
            },
            "Status": {
                "status": {
                    "name": "Done"
                }
            },
            "Difficulty": {
                "select": {
                    "name": difficulty
                }
            },
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": question_title,
                            "link": {
                                "url": leetcode_URL
                            }
                        }
                    }
                ]
            }
        }
    }
    return properties

# Function to add an entry into the Notion database
def add_entry_into_database(databaseId, properties):
    URL = config('URL')

    new_row_data = {
        "parent": {
            "type": "database_id",
            "database_id": databaseId
        },
        **properties
    }

    json_data = json.dumps(new_row_data, indent=4)

    # Print the JSON data
    print("\n\n------------------- JSON Data of the API Request -------------------\n\n")
    print(json_data)
    print("\n\n-------------------------------------------------------------------\n\n")

    headers = {
        "Authorization": "Bearer " + notion_key,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    print("\n\n------------------- Sending API Request to Notion -------------------\n\n")

    # Send a POST request to create the new row in the Notion database
    response = requests.post(URL, json=new_row_data, headers=headers)

    print("\n\n-------------------  Request Sent Successfully! -------------------\n\n")
    # Check the response status
    if response.status_code == 200:
        print("\n\n-------------------  New Entry Made Successfully! -------------------\n\n")
    else:
        print(f"Failed to create new row. Status code: {response.status_code}")

# Main function
def main():
    leetcode_URL = input("Enter the LeetCode URL: ")
    question_id, question_title, tags, difficulty = fetchPageData(leetcode_URL)
    properties = create_properties_data(leetcode_URL, question_id, tags, difficulty, question_title)
    add_entry_into_database(database_id, properties)

if __name__ == "__main__":
    main()
