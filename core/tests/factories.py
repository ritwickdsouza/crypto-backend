import factory

from core.models import Currency, ExchangeRate


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency


class ExchangeRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExchangeRate
