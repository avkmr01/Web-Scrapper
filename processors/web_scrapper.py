from tqdm import tqdm
import json

import requests
from bs4 import BeautifulSoup
from utils.utils import get_timestamp_and_link, getnews
from datetime import datetime, timedelta
import pandas as pd

class GetData():
    def __init__(self, columns):
        self.columns = columns
        self.options = {
            "get_timestamp_and_link": get_timestamp_and_link,
            "getnews": getnews
        }
        self.df = pd.DataFrame(columns=self.columns)


    def get_data(self, url, tag, attributename, filtername, functions, dataframe_name='temporary.xlsx', delta=0):
        # today_date = datetime.today().date()
        # print("Today's date:", today_date - timedelta(days=delta))
        print(url)
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            extractions = soup.find_all(tag, attrs={attributename: filtername})
            for extract in tqdm(extractions):
                for function in functions:
                    actual_func = self.options[function]
                    output = actual_func(extract)
                    if output is not None:
                        output = tuple([url]+output)
                        self.df.loc[len(self.df)] = output
            self.df.to_excel(dataframe_name, index=False)
        else:
            print("Failed to retrieve webpage. Status code:", response.status_code)

            
