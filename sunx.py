from requests import get
import datetime

def get_sunset_delay():
    now = datetime.datetime.now()
    data = get("https://api.sunrise-sunset.org/json?lat=49.204140&lng=-122.788265&formatted=0&date="+now.strftime("%Y-%m-%d")).json()
    date_time_obj = datetime.datetime.strptime(data["results"]["sunset"], '%Y-%m-%dT%H:%M:%S%z')
    if date_time_obj.timestamp() - date_time_obj.now().timestamp() < 0:
        now = now.replace(day=now.day + 1)
        data = get("https://api.sunrise-sunset.org/json?lat=49.204140&lng=-122.788265&formatted=0&date=" + now.strftime(
            "%Y-%m-%d")).json()
        date_time_obj = datetime.datetime.strptime(data["results"]["sunset"], '%Y-%m-%dT%H:%M:%S%z')
    return date_time_obj.timestamp() - date_time_obj.now().timestamp()

def has_sunset():
    now = datetime.datetime.now()
    data = get("https://api.sunrise-sunset.org/json?lat=49.204140&lng=-122.788265&formatted=0&date=" + now.strftime(
        "%Y-%m-%d")).json()
    date_time_obj = datetime.datetime.strptime(data["results"]["sunset"], '%Y-%m-%dT%H:%M:%S%z')
    if date_time_obj.timestamp() - date_time_obj.now().timestamp() < 0:
        return True
    return False