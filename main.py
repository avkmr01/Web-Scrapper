from tqdm import tqdm
from string import ascii_uppercase

from processors.web_scrapper import GetData
import pandas as pd

# from utils.utils import gemini_convert, upload

if __name__=="__main__":
    # url=r'https://www.mayoclinic.org/diseases-conditions/index?letter='

    # scrapper = GetData(columns=['url', 'link','Heading'])
    # for i in tqdm(ascii_uppercase):
    #     url_page=url+str(i)
    #     scrapper.get_data(url_page, 'div', 'class', 'cmp-link', ["get_hospital_data"])

    df = pd.read_excel('mayo-clinic main page.xlsx')
    mc_pages_link = df['link']
    headings = df['Heading']
    scrapper = GetData(columns=['url', 'heading', 'overview'])
    for url, heading in tqdm(zip(mc_pages_link, headings), total=5):
        scrapper.get_data(url, ['h3', 'p', 'ul'], functions=["get_hospital_data"], delta=heading)

