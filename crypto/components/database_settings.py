# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
import os

import dj_database_url

DATABASE_PROTOCOL = os.getenv('DATABASE_PROTOCOL', 'postgres')
DATABASE_USER = os.getenv('DATABASE_USER', 'user')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DATABASE_DB = os.getenv('DATABASE_DB', 'db')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres')

DATABASE_URL = f'{DATABASE_PROTOCOL}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_DB}'
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}
