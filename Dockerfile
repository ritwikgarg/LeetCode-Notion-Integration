# Use an official Python runtime as a parent image
FROM python:3.9-bullseye

# Install Chrome and necessary libraries
RUN apt-get update -y && apt-get install -y wget unzip curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -y && apt-get install -y google-chrome-stable

# Set the working directory in the container
WORKDIR /

# Copy only the requirements.txt file into the container at /
COPY NotionAPI.py requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents (excluding requirements.txt) into the container at /
COPY . /

# Define environment variables
ENV NOTION_KEY="secret_Lhh49exNTfbihBqxWZywQBwq8JHHVNN7xXfgEvFrfUR"
ENV DATABASE_ID="d79d60d1808d4edd93495ffeae9e13b2"
ENV URL="https://api.notion.com/v1/pages"
ENV LEETCODE_URL="" 

# Run your Python script
CMD ["python", "NotionAPI.py"]
