import os

ALPHA_VANTAGE_BASE_URL = os.getenv('ALPHA_VANTAGE_BASE_URL', 'https://www.alphavantage.co/query')
ALPHA_VANTAGE_TIMEOUT = int(os.getenv('ALPHA_VANTAGE_TIMEOUT', '5'))
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'DEMO')
