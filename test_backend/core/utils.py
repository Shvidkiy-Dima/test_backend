from functools import wraps
from rest_framework.exceptions import ValidationError
import requests


def required_params(required):

    def inner(f):

        @wraps(f)
        def _inner(self, req, *args, **kwargs):
            if not set(required).issubset(set(req.query_params)):
                raise ValidationError(f'Required query params - {required}')

            return f(self, req, *args, **kwargs)

        return _inner

    return inner


def request_json(url, method='get'):
    res = getattr(requests, method.lower())(url)
    res.raise_for_status()
    return res.json()