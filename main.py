import os
from tqdm import tqdm

from processors.web_scrapper import GetData
import pandas as pd

from utils.utils import gemini_convert, upload

if __name__=="__main__":

    # url = r'https://www.moneycontrol.com/stocks/marketstats/nse-gainer/all-companies_-2/'
    # scrapper = GetData(columns = ['main_url', 'link'])
    # scrapper.get_data(url, 'span', 'class', 'gld13 disin', ["get_top_gainer_list"], f'assets/extracted_link_data.xlsx')

    
    df_temp = pd.read_excel(f'assets/extracted_link_data.xlsx')
    link_info_scrapper = GetData(columns = ['link', 'price', 'percent', 'volume', 'transaction', 'screener', 'tradingview'])
    for url in tqdm(df_temp['link']):
        link_info_scrapper.get_data(url, 'div', 'class', 'pnc_wrapper', ["get_mc_page_data"], f'assets/final_extracted.xlsx')
    
    
    # upload([df_temp, df_converted], 'link', ['content','converted_content'], category)