from tqdm import tqdm

from processors.web_scrapper import GetData
import pandas as pd

from utils.utils import gemini_convert, upload

if __name__=="__main__":
    # url = r'https://www.moneycontrol.com/news/politics/'
    # scrapper = GetData(columns=['url','date','time'])
    # scrapper.get_data(url, 'li', 'class_', 'clearfix', ["get_timestamp_and_link"])
    # del url

    # scrapper = GetData(columns=['url', 'content'])
    df_temp = pd.read_excel('temporary.xlsx')
    # for url in df_temp['url']:
    #     scrapper.get_data(url, 'script', 'type', 'application/ld+json', ["getnews"], 'scrapped_url.xlsx')

    # df_scrapped = pd.read_excel('scrapped_url.xlsx')
    # converted_content = []
    # for content in tqdm(df_scrapped['content']):
    #     converted_content.append(gemini_convert(content))
    # df_scrapped['converted_content'] = converted_content
    # df_scrapped.to_excel('converted_content.xlsx')

    df_converted = pd.read_excel('converted_content.xlsx')

    upload([df_temp, df_converted], 'politics')