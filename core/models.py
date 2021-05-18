from django.db import models

from core.clients.alpha_vantage import AlphaVantageClient


class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.code} | {self.name}'


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='from_currency')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='to_currency')
    value = models.DecimalField(decimal_places=10, max_digits=20)
    refreshed_at = models.DateTimeField()

    def __str__(self):
        return f'{self.from_currency} | {self.to_currency} | {self.value} | {self.refreshed_at}'

    @classmethod
    def fetch_and_update(cls, from_currency_code, to_currency_code):
        try:
            from_currency = Currency.objects.get(code=from_currency_code)
            to_currency = Currency.objects.get(code=to_currency_code)
        except Currency.DoesNotExist:
            return None
        
        alpha_vantage_client = AlphaVantageClient()
        exchange_rate = alpha_vantage_client.get_exchange_rate(
            from_currency=from_currency_code,
            to_currency=to_currency_code
        )

        if not exchange_rate:
            return None

        return cls.objects.create(
            from_currency=from_currency,
            to_currency=to_currency,
            value=exchange_rate.value,
            refreshed_at=exchange_rate.refreshed_at
        )
