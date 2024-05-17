import json
import os
from dotenv import load_dotenv
import textwrap

from datetime import datetime, timedelta
import pytz
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import markdown2
from bs4 import BeautifulSoup
import pypandoc
from pypandoc.pandoc_download import download_pandoc

download_pandoc()
load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_KEY')
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

today_date = datetime.today().date()
today_date = today_date - timedelta(days=0)
today_date = today_date.strftime("%d-%m-%Y")

def to_markdown(markdown_text):
    markdown_text = markdown_text.replace('**','*')
    html_text = markdown2.markdown(markdown_text)
    # plain_text = pypandoc.convert_text(html_text, 'rtf', format='html')
    plain_text = BeautifulSoup(html_text, "html.parser")
    plain_text = plain_text.get_text()

    # plain_text = plain_text.prettify()
    return str(plain_text)

def get_timestamp_and_link(extraction):
    link = extraction.find('a')['href']
    timestamp = extraction.find('span').text
    timestamp=timestamp.replace(" IST", "")
    date_object = datetime.strptime(timestamp, "%B %d, %Y %I:%M %p")
    india_timezone = pytz.timezone('Asia/Kolkata')  # IST corresponds to Indian Standard Time
    date_object = india_timezone.localize(date_object)
    utc_date_object = date_object.astimezone(pytz.utc)
    formatted_date = utc_date_object.strftime("%d-%m-%Y")
    formatted_time = utc_date_object.strftime("%H:%M:%S")
    if today_date == formatted_date:
        return [link, formatted_date, formatted_time]
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
            return [article_body]
    return None

def gemini_convert(message):
    try:
        prompt = f"summarise informatively the '{message}' in a more easy understable way. and provide some future possibilities. don't bold the heading and make heading a list"
        response = model.generate_content(prompt)
        text = to_markdown(response.text)
    except:
        text = "harmful content"
    return text

def upload(dataframes, mergecol, main_col, spreadsheet_name):
    merged_df = pd.merge(*dataframes, on=mergecol)
    main_df = merged_df[main_col]
    main_df_cols = main_df.columns
    row_date = pd.DataFrame({main_df_cols[0]:["Date"], main_df_cols[1]: [today_date]})
    main_df = pd.concat([row_date, main_df], ignore_index=True)
    modified_dataframes = [main_df, merged_df]
    for idx, dataframe in enumerate(modified_dataframes):
        dataframe = dataframe.dropna()
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

        if idx == 0:
            worksheet.clear()

        # Append data to the worksheet
        worksheet.append_rows(data_to_append)

        print("Data appended successfully.")