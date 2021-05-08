import http
from copy import deepcopy
from functools import partial
from logging import getLogger
from typing import Dict

import requests
from django.conf import settings

logger = getLogger(__name__)


class ClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class APIClientError(ClientError):
    def __init__(self, message, status, detail):
        super(APIClientError, self).__init__(message)
        self.message = message
        self.status = status
        self.detail = detail

    def __str__(self):
        return f'{self.__class__.__name__} status: {self.status}, message: {self.message}, detail: {self.detail}'


class BaseAPIClient:
    BASE_URL = None
    TIMEOUT = 60
    HEADERS = {}

    def __init__(self):
        if not self.BASE_URL:
            raise ClientError(f'BASE_URL not defined in {self.__class__.__name__}')

    def __getattr__(self, attr):
        attr_lower = attr.lower()
        if attr_lower in ('get', 'post', 'put', 'options', 'delete'):
            return partial(self.request, method=attr_lower)
        return self.__getattribute__(attr_lower)

    def _construct_headers(self, headers):
        _headers = deepcopy(self.HEADERS)
        if headers:
            _headers.update(headers)
        return _headers

    def request(self, *args, **kwargs):
        headers = self._construct_headers(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        kwargs['timeout'] = kwargs.get('timeout', None) or self.TIMEOUT
        try:
            resp = requests.request(*args, **kwargs)
            resp.raise_for_status()
        except requests.exceptions.RequestException as exception:
            message = http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase
            status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
            detail = str(exception)
            raise APIClientError(message=message, status=status_code, detail=detail)
        logger.debug('Response %s from server with content %s', resp.status_code, resp.content)
        return resp.json()
