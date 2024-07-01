import re
import json
import os
from dotenv import load_dotenv
import textwrap
import requests

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

def get_top_gainer_list(extraction):
    link = extraction.find('a')['href']
    return [link]

def get_screener_page_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        roce_text = soup.find('span', text='ROCE')
        roce = roce_text.find_next_sibling('span').text.strip()
        print('ROCE', roce)
    else:
        return '',''

def get_mc_page_data(extraction):
    price = extraction.find('div', class_='inprice1 nsecp').get('rel')
    points_n_percent = extraction.find('div', id='nsechange').text
    splitted = re.split('[ (|%)]',points_n_percent)
    points, percent = list(filter(None,splitted))
    volume = extraction.find('div', class_='rangamount nsevol').text.replace(',', '')
    nse_element = extraction.find('span', text="NSE:")
    short_hand = 'Not Found'
    if nse_element:
        short_hand = nse_element.find_next_sibling('p').text.strip()
        screener_url = f'https://www.screener.in/company/{short_hand}/'
        tradingview_url = f'https://in.tradingview.com/chart/yN9sgSm2/?symbol=NSE%3A{short_hand}'
    else:
        screener_url='NOT FOUND'
        tradingview_url='NOT FOUND'
        
    # pe, roce = get_screener_page_data(screener_url)
    return [price, points, percent, volume, float(price)*int(volume), screener_url, tradingview_url]

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