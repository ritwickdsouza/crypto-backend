import csv
import os
import sys

from django.db import migrations


# Currency list from Alpha Vantage
CURRENCY_LIST_PATH = 'data/currency_list.csv'


def get_currency_list_csv_path():
    return os.path.join(os.path.dirname(__file__), CURRENCY_LIST_PATH)


def create_currencies(apps, schema_editor):
    Currency = apps.get_model('core', 'Currency')

    with open(get_currency_list_csv_path(), 'r') as csv_file:
        csv_dict_reader = csv.DictReader(csv_file)
        sys.stdout.write('\n')
        for row in csv_dict_reader:
            name = row['name']
            code = row['code']
            try:
                Currency.objects.create(name=name, code=code)
                sys.stdout.write(f'Currency `{name}` with code `{code}` created\n')
            except Exception as e:
                sys.stderr.write(f'Currency `{name}` with code `{code}` failed to create. Exception: {e}\n')


def remove_currencies(apps, schema_editor):
    Currency = apps.get_model('core', 'Currency')

    with open(get_currency_list_csv_path(), 'r') as csv_file:
        csv_dict_reader = csv.DictReader(csv_file)
        sys.stdout.write('\n')
        for row in csv_dict_reader:
            name = row['name']
            code = row['code']
            try:
                currency = Currency.objects.get(code=code)
                currency.delete()
                sys.stdout.write(f'Currency `{name}` with code `{code}` deleted\n')
            except Exception as e:
                sys.stderr.write(f'Currency `{name}` with code `{code}` failed to delete. Exception: {e}\n')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_create_currency_exchange_rate_models')
    ]

    operations = [
        migrations.RunPython(create_currencies, reverse_code=remove_currencies)
    ]
