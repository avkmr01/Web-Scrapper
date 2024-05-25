import json
import os
import re
from dotenv import load_dotenv

import textwrap
from datetime import datetime, timedelta
from IPython.display import Markdown, display
import pytz
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
genai.configure(api_key=GEMINI_KEY)
# model = genai.GenerativeModel('gemini-pro')

today_date = datetime.today().date()

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_timestamp_and_link(extraction):
    link = extraction.find('a')['href']
    timestamp = extraction.find('span').text
    timestamp=timestamp.replace(" IST", "")
    date_object = datetime.strptime(timestamp, "%B %d, %Y %I:%M %p")
    india_timezone = pytz.timezone('Asia/Kolkata')  # IST corresponds to Indian Standard Time
    date_object = india_timezone.localize(date_object)
    utc_date_object = date_object.astimezone(pytz.utc)
    formatted_date = utc_date_object.strftime("%Y-%m-%d")
    formatted_time = utc_date_object.strftime("%H:%M:%S")
    # print(today_date, formatted_date, type(today_date), type(formatted_date), str(today_date) == formatted_date)
    if str(today_date) == formatted_date:
        return (formatted_date, formatted_time)
    else:
        return None

def getnews(extraction):
    json_data = extraction.string

    # Parse the JSON data
    parsed_data = json.loads(json_data, strict=False)

    # Extract the value of the "articleBody" key
    if len(parsed_data)!=0 and isinstance(parsed_data,list):
        if 'articleBody' in parsed_data[0]:
            article_body = parsed_data[0]['articleBody']
            article_body = article_body.replace(r'&nbsp;', ' ')
            article_body = article_body.replace(r'&amp;quot;', '"')
            return (article_body)
    return None

# def gemini_convert(message):
#     prompt = f"summarise informatively the '{message}' in a more easy understable way. and provide some future possibilities."
#     response = model.generate_content(prompt)
#     return (response.text)

def upload(dataframes, spreadsheet_name):
    for idx, dataframe in enumerate(dataframes):
        # Authenticate using your credentials JSON file
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('sacred-garden-240417-dd1a4c6d6b06.json', scope)
        client = gspread.authorize(credentials)

        # Open the specified spreadsheet
        spreadsheet = client.open(spreadsheet_name)

        # Select the worksheet where you want to append data
        worksheet = spreadsheet.get_worksheet(idx)  # Change the index (0) if needed

        # Convert DataFrame to list of lists (each inner list represents a row)
        data_to_append = dataframe.values.tolist()

        # Append data to the worksheet
        worksheet.append_rows(data_to_append)

        print("Data appended successfully.")


def get_hospital_data(extraction, delta=None):
    ## parkway east
    # heading = extraction.find('p', attrs={'class': 'result-page-title'}).string
    # tag = extraction.find('span', attrs={'class': 'page-tag-item'}).string
    # content = extraction.find('p', attrs={'class': 'result-page-content'}).string
    # return (heading, tag, content)

    ## mayo healthcare - main page
    # link = extraction.find('a')['href']
    # heading = extraction.string
    # print(heading, link)
    # return (link, heading)

    ## mayo healthcare - page depth level 1
    start_list = ['try again in a couple of minutes', 'Clinic Health Letter']
    end_list = ['information submitted for this request', 'Products & Services', 'Mayo ClinicConnect', 'Mayo Clinic', 'Patient Care & Health Information']
    text = ''
    temp = 1
    for element in extraction:
        # if any(end in element.text.strip() for end in end_list):
        #     temp = 0
        if re.search('h[1-6]', element.name) and temp == 1:
            text+='\n'
            text+=element.text.strip()  # Print heading with stripped text
            text+='\n'
            
        elif element.name == 'ul' and temp == 1:
            text+='\n'
            all_li = element.find_all('li')
            li = ['* ' + word.text.strip() + '\n' for word in all_li]
            for single_li in li:
                text+=single_li # Print list items with indentation
            
        elif temp == 1:
            text+='\n'
            text+=element.text.strip()  # Print paragraph with stripped text
            text+='\n'
        # if any(start in element.text.strip() for start in start_list):
        #     temp = 1 
        # if element.text.strip() == delta:
        #     temp = 1
        
    if text != '':
        return [text]
    else:
        return ['found nothing']
