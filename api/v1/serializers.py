from rest_framework import serializers

from core.models import Currency


class CurrencySerializer(serializers.Serializer):
    pass


class QuoteSerializer(serializers.Serializer):
    from_currency = CurrencySerializer()
    to_currency = CurrencySerializer()

