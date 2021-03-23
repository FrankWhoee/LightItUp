from requests import get
import datetime

def get_sunset_delay():
    data = get("https://api.sunrise-sunset.org/json?lat=49.204140&lng=-122.788265&formatted=0").json()
    date_time_obj = datetime.datetime.strptime(data["results"]["sunset"], '%Y-%m-%dT%H:%M:%S+00:00')
    return date_time_obj.timestamp() - date_time_obj.now().timestamp()

