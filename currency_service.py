import os
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Load the variables from .env file into the environment
load_dotenv()

# Getting credentials
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
api_key = os.getenv('EXCHANGE_RATE_API_KEY')

# Country id map 
currency_country_map = {
    'KZT': 1,
    'UZS': 3,
    'AZN': 5,
    'MYR': 6,
}

# Get latest currency rates through API , historical data is not available using free plan
def get_currency_rates(currencies):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)
    data = response.json()
    rates = {}
    for currency in currencies:
        rates[currency] = data['conversion_rates'][currency]
    return rates

# Create a table if not exists
def create_table_if_not_exists():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_rates (
            ds DATE NOT NULL,
            country_id INTEGER NOT NULL,
            currency VARCHAR(3) NOT NULL,
            rate NUMERIC NOT NULL,
            PRIMARY KEY (ds, currency)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def store_to_db(currency_data):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()

    for data in currency_data:
        cursor.execute("INSERT INTO currency_rates (ds, country_id, currency, rate) VALUES (%s, %s, %s, %s)",
                       (data['ds'], data['country_id'], data['currency'], data['rate']))
    
    conn.commit()
    cursor.close()
    conn.close()

# Main function of the service
def main(currencies, ds):
    create_table_if_not_exists()
    currency_data = []
    latest_rates = get_currency_rates(currencies)
    for currency in currencies:
        country_id = currency_country_map[currency]
        currency_data.append({"ds": ds, "country_id": country_id, "currency": currency, "rate": latest_rates[currency]})
    store_to_db(currency_data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--currencies", nargs='+', type=str, required=True, help="List of currency codes")
    parser.add_argument("--ds", type=str, required=True, help="Date for which to fetch the rates in format YYYY-MM-DD")
    args = parser.parse_args()
    
    main(args.currencies, args.ds)
