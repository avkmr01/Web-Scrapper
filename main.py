import os
from tqdm import tqdm

from processors.web_scrapper import GetData
import pandas as pd

from utils.utils import gemini_convert, upload

if __name__=="__main__":
    news_categories = [r'politics/', r'business/companies/', r'business/ipo/', r'business/economy/']
    for news_category in news_categories:
        category = os.path.basename(news_category.rstrip('/'))
        print(f'**************************************Extracting {category} news**************************************')
        print(category)
        url = f'https://www.moneycontrol.com/news/{news_category}'
        scrapper = GetData(columns=['main_url', 'link','date','time'])
        scrapper.get_data(url, 'li', 'class', 'clearfix', ["get_timestamp_and_link"], f'assets/{category}_link_date.xlsx')
        del url

        scrapper = GetData(columns=['link', 'content'])
        df_temp = pd.read_excel(f'assets/{category}_link_date.xlsx')
        for url in df_temp['link']:
            scrapper.get_data(url, 'script', 'type', 'application/ld+json', ["getnews"], f'assets/{category}_scrapped_url.xlsx')

        df_scrapped = pd.read_excel(f'assets/{category}_scrapped_url.xlsx')
        converted_content = []
        for content in tqdm(df_scrapped['content']):
            converted_content.append(gemini_convert(content))
        df_scrapped['converted_content'] = converted_content
        df_scrapped.to_excel(f'assets/{category}_converted_content.xlsx', index=False)

        df_converted = pd.read_excel(f'assets/{category}_converted_content.xlsx')
        upload([df_temp, df_converted], 'link', ['content','converted_content'], category)