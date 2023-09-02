# LeetCode to Notion Integration

This Python script allows you to fetch data from a LeetCode question page and add it to a Notion database.

## Prerequisites

Before running this script, you need to have the following dependencies installed:

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/) for web automation
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) for HTML parsing
- [Requests](https://pypi.org/project/requests/) for making HTTP requests
- [Decouple](https://pypi.org/project/python-decouple/) for managing sensitive information
- [WebDriver Manager](https://pypi.org/project/webdriver-manager/) for managing webdrivers (specifically for Chrome or Firefox)

Make sure to install these dependencies using `pip`:

```bash
pip install selenium beautifulsoup4 requests python-decouple webdriver-manager
```
## Configuration
Sensitive information such as your Notion API key and Notion database ID should be stored in a .env file. You can use the provided .env.example as a template.

## Usage
<ul>
<li>
Clone this repository to your local machine.  
</li>
<li>
Create a .env file in the project directory and populate it with your Notion API key and database ID.  
</li>
<li>
Open a terminal and navigate to the project directory.
</li>
<li>
Run the script with the following command:
</li>
  
```bash
python NotionAPI.py
```
<li>
You will be prompted to enter the LeetCode URL of the question you want to add to your Notion database.
</li>  
<li>
The script will fetch data from the LeetCode page, create a corresponding entry, and add it to your Notion database.
</li>
</ul>
