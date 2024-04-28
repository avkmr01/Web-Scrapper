from processors.web_scrapper import GetData

if __name__=="__main__":
    url = r'https://www.moneycontrol.com/news/politics/'
    scrapper = GetData(url, columns=['url','date','time'])
    scrapper.get_data('li', 'clearfix', ["get_timestamp_and_link"])