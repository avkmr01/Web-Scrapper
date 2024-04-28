from datetime import datetime, timedelta
import pytz

today_date = datetime.today().date()

def get_timestamp_and_link(headline):
    link = headline.find('a')['href']
    timestamp = headline.find('span').text
    timestamp=timestamp.replace(" IST", "")
    date_object = datetime.strptime(timestamp, "%B %d, %Y %I:%M %p")
    india_timezone = pytz.timezone('Asia/Kolkata')  # IST corresponds to Indian Standard Time
    date_object = india_timezone.localize(date_object)
    utc_date_object = date_object.astimezone(pytz.utc)
    formatted_date = utc_date_object.strftime("%Y-%m-%d")
    formatted_time = utc_date_object.strftime("%H:%M:%S")
    # print(today_date, formatted_date, type(today_date), type(formatted_date), str(today_date) == formatted_date)
    if str(today_date) == formatted_date:
        return (link, formatted_date, formatted_time)
    else:
        return None