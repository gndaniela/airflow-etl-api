import os
import json
import requests
from time import sleep
from src.config import API_KEY


def write_json(target_path: str, target_file: str, data):
    # if directory doesn't exist, create it
    full_dir = os.path.join(target_path, target_file)
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    if not os.path.exists(full_dir):
        with open(full_dir, "w") as f:
            data = json.dumps(data)
            f.write(f"[{data}]")
    else:
        with open(full_dir, "r") as f:
            dictObj = json.load(f)
        with open(full_dir, "w") as f:
            dictObj.append(data)
            json.dump(dictObj, f, indent=6)


def get_symbol_data(symbol: str, root_dir: str, **context):
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={API_KEY}"
    r = requests.get(url)
    sleep(61)  # Handle API limit for catchups in Airflow
    data = r.json()
    last_info = data["Time Series (Digital Currency Daily)"]
    last_info = last_info[context["ds"]]
    date = str(context["ds"])
    print(date)
    last_info["date"] = date
    last_info["crypto_code"] = symbol
    last_info["crypto_name"] = data["Meta Data"]["3. Digital Currency Name"]
    print(last_info)
    print("End of function OK")
    # write new data to file
    write_json(os.path.join(root_dir, "tmp"), "cryptos.json", last_info)
