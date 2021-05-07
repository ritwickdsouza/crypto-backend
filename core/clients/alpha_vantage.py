from logging import getLogger

from django.conf import settings

from core.clients.base import BaseAPIClient, APIClientError
from core.clients.data_models import ExchangeRate, Currency

logger = getLogger(__name__)


class AlphaVantageClient(BaseAPIClient):
    BASE_URL = settings.ALPHA_VANTAGE_BASE_URL
    TIMEOUT = 60

    def get_exchange_rate(self, from_currency: str, to_currency:str) -> ExchangeRate:
        exchange_rate = None
        try:
            response = self.get(
                url=self.BASE_URL,
                params={
                    'function': 'CURRENCY_EXCHANGE_RATE',
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'apikey': settings.ALPHA_VANTAGE_API_KEY
                }
            )
            data = response['Realtime Currency Exchange Rate']
            exchange_rate = ExchangeRate(
                from_currency=Currency(
                    code=data['1. From_Currency Code'],
                    name=data['2. From_Currency Name']
                ),
                to_currency=Currency(
                    code=data['3. To_Currency Code'],
                    name=data['4. To_Currency Name']
                ),
                value=data['5. Exchange Rate'],
                refreshed_at=data['6. Last Refreshed']
            )
        except (APIClientError, KeyError):
            logger.exception('Error during getting exchange rate from_currency:%s and to_currency', from_currency, to_currency)

        return exchange_rate
