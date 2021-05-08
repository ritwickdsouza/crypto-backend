from logging import getLogger

from celery import shared_task

from core.models import Currency, ExchangeRate

logger = getLogger(__name__)

EXCHANGE_RATES_TO_UPDATE = [
    ('BTC', 'USD')
]

@shared_task
def update_exchange_rates():
    for from_currency_code, to_currency_code in EXCHANGE_RATES_TO_UPDATE:
        exchange_rate = ExchangeRate.fetch_and_update(
            from_currency_code=from_currency_code,
            to_currency_code=to_currency_code
        )
        if exchange_rate:
            logger.info('Exchange Rate updated for %s | %s ', from_currency_code, to_currency_code)
        else:
            logger.exception('Exchange Rate failed to update for %s | %s ', from_currency_code, to_currency_code)
