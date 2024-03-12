import os
from dotenv import load_dotenv
load_dotenv()

stock_price_path = os.getenv("STOCK_PRICE")

with open(stock_price_path, 'r') as file:
  stock_price = file.read()

# print(stock_price)

