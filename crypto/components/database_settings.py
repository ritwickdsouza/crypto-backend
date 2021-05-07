# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
import os

import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://postgres:password@database/postgres')
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}
