from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Currency
from core.models import ExchangeRate


class CurrencySerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = Currency
        fields = ['code', 'name']


class QuotesSerializer(serializers.ModelSerializer):
    from_currency = CurrencySerializer(read_only=True)
    to_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = ExchangeRate
        fields = ['from_currency', 'to_currency', 'value']


class QuotesAPIViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = QuotesSerializer

    def get_object(self):
        from_currency_code = self.request.GET.get('from_currency')
        to_currency_code = self.request.GET.get('to_currency')

        return self.get_queryset().filter(
            from_currency__code=from_currency_code,
            to_currency__code=to_currency_code
        ).order_by('refreshed_at').last()

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, *args, **kwargs):
        from_currency_code = self.request.GET.get('from_currency')
        to_currency_code = self.request.GET.get('to_currency')

        ExchangeRate.fetch_and_update(
            from_currency_code=from_currency_code,
            to_currency_code=to_currency_code
        )
        return self.retrieve(*args, **kwargs)
