from tqdm import tqdm
import json

import requests
from bs4 import BeautifulSoup
from utils.utils import get_timestamp_and_link, getnews, get_hospital_data
from datetime import datetime, timedelta
import pandas as pd

class GetData():
    def __init__(self, columns, df_name=None):
        self.columns = columns
        self.options = {
            "get_timestamp_and_link": get_timestamp_and_link,
            "getnews": getnews,
            "get_hospital_data": get_hospital_data
        }
        if df_name is not None:
            self.df = pd.read_excel(df_name, usecols=self.columns)
        self.df = pd.DataFrame(columns=self.columns)


    def get_data(self, url, tag, attributename=None, filtername=None, functions=[], dataframe_name='temporary.xlsx', delta=None):
        # today_date = datetime.today().date()
        # print("Today's date:", today_date - timedelta(days=delta))
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.find_all(tag))
            if attributename is not None:
                extractions = soup.find_all(tag, attrs={attributename: filtername})
            else:
                extractions = [soup.find_all(tag)]
            if len(functions) > 0:
                for extract in extractions:
                    for function in functions:
                        actual_func = self.options[function]
                        output = actual_func(extract, delta)
                        if output is not None:
                            if delta is not None:
                                output = tuple([url, delta, *output])
                            else:
                                output = tuple([url, *output])
                            # print(output)
                            self.df.loc[len(self.df)] = output
                    

            self.df.to_excel(dataframe_name, index=False)
        else:
            print("Failed to retrieve webpage. Status code:", response.status_code)

            
