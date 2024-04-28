from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
from utils.utils import get_timestamp_and_link
from datetime import datetime, timedelta
import pandas as pd

class GetData():
    def __init__(self, url, columns):
        self.url=url
        self.columns = columns
        self.options = {
            "get_timestamp_and_link": get_timestamp_and_link
        }


    def get_data(self, tag, classname, functions, dataframe_name='temporary.xlsx', secondary_url='', delta=0):
        url = self.url+r'/'+secondary_url
        df = pd.DataFrame(columns=self.columns)
        # today_date = datetime.today().date()
        # print("Today's date:", today_date - timedelta(days=delta))

        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            extractions = soup.find_all(tag, class_=classname)
            for extract in tqdm(extractions):
                for function in functions:
                    actual_func = self.options[function]
                    output = actual_func(extract)
                    if output is not None:
                        df.loc[len(df)] = output
            df.to_excel(dataframe_name, index=False)
        else:
            print("Failed to retrieve webpage. Status code:", response.status_code)