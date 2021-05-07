# Python
FROM python:3.9.5
ENV PYTHONUNBUFFERED 1

# User
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
WORKDIR /home/user/app

# Essentials
RUN apt-get update -y
RUN apt-get install gcc build-essential libpq-dev -y
RUN python3 -m pip install --no-cache-dir pip-tools

# Project requirements
ADD ./requirements.txt /home/user/app/
RUN pip install -r requirements.txt

# Source code
ADD . /home/user/app

# User
USER user

# Web server
CMD ["sh", "-c", "gunicorn crypto.wsgi -b 0.0.0.0:8000"]
