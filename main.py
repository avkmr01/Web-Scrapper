import os
from tqdm import tqdm
from time import time

from processors.web_scrapper import GetData
import pandas as pd

from utils.utils import gemini_convert, upload

def calculate_action(leap_0, leap_1):
  """Calculates the action value based on the signs of leap_0 and leap_1.

  Args:
      leap_0: A numerical value representing the first leap.
      leap_1: A numerical value representing the second leap.

  Returns:
      1 if both leap_0 and leap_1 are positive, -1 if one is negative, 0 otherwise.
  """
  if leap_0 > 0 and leap_1 > 0:
    return 1
  elif leap_0 < 0 or leap_1 < 0:
    return -1
  else:
    return 0

if __name__=="__main__":
    # start = time.now()
    
    url = r'https://www.moneycontrol.com/stocks/marketstats/nse-gainer/all-companies_-2/'
    scrapper = GetData(columns = ['main_url', 'link'])
    scrapper.get_data(url, 'span', 'class', 'gld13 disin', ["get_top_gainer_list"], f'assets/extracted_link_data.xlsx')

    df_temp = pd.read_excel(f'assets/extracted_link_data.xlsx')
    for i in range(0,3):
        link_info_scrapper = GetData(columns = ['link', 'price', 'percent', 'transaction', 'screener', 'tradingview'])
        for url in tqdm(df_temp['link']):
            link_info_scrapper.get_data(url, 'div', 'class', 'pnc_wrapper', ["get_mc_page_data"], f'assets/final_extracted_{i}.xlsx')
        time.sleep(60*15)
    
    temp_0 = pd.read_excel(r'assets/final_extracted_0.xlsx')
    temp_1 = pd.read_excel(r'assets/final_extracted_1.xlsx')
    temp_2 = pd.read_excel(r'assets/final_extracted_2.xlsx')

    temp_0['percent 0'] = temp_0['percent']
    temp_0['percent 1'] = temp_1['percent']
    temp_0['percent 2'] = temp_2['percent']
    temp_0['leap 0'] = temp_0['percent 1'] - temp_0['percent 0']
    temp_0['leap 1'] = temp_0['percent 2'] - temp_0['percent 1']
    temp_0['action'] = temp_0.apply(lambda row: calculate_action(row['leap 0'], row['leap 1']), axis=1)

    temp_0.to_excel(r'assets/final_analysed.xlsx', index = False)

    # end = time.now()

    # print('Time taken ', end-start)