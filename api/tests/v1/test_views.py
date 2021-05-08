from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from rest_framework.test import APITestCase

from core.clients.data_models import Currency as CurrencyDataModel
from core.clients.data_models import ExchangeRate as ExchangeRateDataModel
from core.models import Currency
from core.tests.factories import ExchangeRateFactory


class QuotesAPIViewTestCase(APITestCase):
    def setUp(self):
        self.btc = Currency.objects.get(code='BTC')
        self.usd = Currency.objects.get(code='USD')

    def test_get_quote_exchange_no_query_params(self):
        # given / when
        response = self.client.get(reverse('quotes'))

        # then
        self.assertEqual(response.status_code, 404)

    def test_get_quote_exchange_correct_query_params_currency_not_found(self):
        # given
        base_url = reverse('quotes')
        query_params = {
            'from_currency': 'ABC',
            'to_currency': 'XYZ'
        }
        url = f'{base_url}?{urlencode({**query_params})}'

        # when
        response = self.client.get(url)

        # then
        self.assertEqual(response.status_code, 404)

    def test_get_quote_exchange_correct_query_params_exchange_not_found(self):
        # given
        base_url = reverse('quotes')
        query_params = {
            'from_currency': 'BTC',
            'to_currency': 'USDT'
        }
        url = f'{base_url}?{urlencode({**query_params})}'

        # when
        response = self.client.get(url)

        # then
        self.assertEqual(response.status_code, 404)

    def test_get_quote_exchange_correct_query_params_exchange_found(self):
        # given / when
        ExchangeRateFactory.create(
            from_currency=self.btc,
            to_currency=self.usd,
            value=1000.0,
            refreshed_at=timezone.now()
        )

        base_url = reverse('quotes')
        query_params = {
            'from_currency': 'BTC',
            'to_currency': 'USD'
        }
        url = f'{base_url}?{urlencode({**query_params})}'

        # when
        response = self.client.get(url)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'from_currency': {
                    'code': 'BTC',
                    'name': 'Bitcoin'
                },
                'to_currency': {
                    'code': 'USD',
                    'name': 'United States Dollar'
                },
                'value': '1000.0000000000'
            }
        )

    @patch('core.models.AlphaVantageClient')
    def test_post_quote_exchange_correct_query_params_exchange_found(self, mocked_alpha_vantage_client_class):
        # given / when
        ExchangeRateFactory.create(
            from_currency=self.btc,
            to_currency=self.usd,
            value=1000.0,
            refreshed_at=timezone.now()
        )
        mocked_alpha_vantage_client_class.return_value.get_exchange_rate.return_value = ExchangeRateDataModel(
            from_currency=CurrencyDataModel(
                code='BTC',
                name='Bitcoin'
            ),
            to_currency=CurrencyDataModel(
                code='USD',
                name='United States Dollar'
            ),
            value='2000.0',
            refreshed_at=timezone.now()
        )

        base_url = reverse('quotes')
        query_params = {
            'from_currency': 'BTC',
            'to_currency': 'USD'
        }
        url = f'{base_url}?{urlencode({**query_params})}'

        # when
        response = self.client.post(url)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                'from_currency': {
                    'code': 'BTC',
                    'name': 'Bitcoin'
                },
                'to_currency': {
                    'code': 'USD',
                    'name': 'United States Dollar'
                },
                'value': '2000.0000000000'
            }
        )
