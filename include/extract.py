import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

csv_filepath = "/usr/local/airflow/include/data/retail_sales.csv"

api_url = "https://dummyjson.com/products"

def extract_csv():
    df = pd.read_csv(csv_filepath)
    return df

def extract_api():
    session = requests.Session()

    retry = Retry(
        total = 5,
        backoff_factor=1,
        status_forcelist = [500,502,503,504]
    )

    session.mount("https://" , HTTPAdapter(max_retries=retry))

    headers = {"User-Agent" : "Mozilla/5.0"}
    response = session.get(api_url, headers= headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data["products"])