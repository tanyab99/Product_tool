import sys
import os
import pandas as pd
import requests
from dotenv import load_dotenv
from utils import read_and_clean_data

load_dotenv()

API_KEY = os.getenv('API_KEY')

def get_external_data():
    url = f'https://test.priceapi.com/products?apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch external data.")

def compare_prices(data, external_data):
    price_alerts = []
    for _, row in data.iterrows():
        product_name = row['product_name']
        our_price = row['our_price']
        market_price = next((item['price'] for item in external_data if item['name'] == product_name), None)
        if market_price:
            if our_price < market_price:
                price_alerts.append(f"{product_name}: Our price is LOWER than market price by ${market_price - our_price:.2f}.")
            elif our_price > market_price:
                price_alerts.append(f"{product_name}: Our price is HIGHER than market price by ${our_price - market_price:.2f}.")
            else:
                price_alerts.append(f"{product_name}: Our price is equal to market price.")
    return price_alerts

def write_report(price_alerts, file_path='report.md'):
    with open(file_path, 'w') as f:
        f.write("# Price Comparison Report\n\n")
        f.write("## Price Alerts\n")
        for alert in price_alerts:
            f.write(f"- {alert}\n")

def main(csv_file):
    data = read_and_clean_data(csv_file)
    external_data = get_external_data()
    price_alerts = compare_prices(data, external_data)
    write_report(price_alerts)

if __name__ == "__main__":
    csv_file = sys.argv[1]
    main(csv_file)

