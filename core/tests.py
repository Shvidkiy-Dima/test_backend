import sys
import re
import json
from os.path import join
from random import uniform
from unittest.mock import patch
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status
from geopy.distance import geodesic
from custom_user.tests import LoginTest
from .models import Company


class TestCore(LoginTest):
    fixtures = ['fixtures.json']

    def test_nearest_companies(self):
        res = self.client.get('/company/nearest/')
        self.assertTrue(status.is_client_error(res.status_code))
        x, y = uniform(-180, 180), uniform(-90, 90)
        res = self.client.get('/company/nearest/', data={'coordinates': f'{x},{y}'})
        to, km = res.data[0]['geo']['to'], res.data[0]['geo']['distance']
        check_distance = geodesic((y, x), reversed(to)).km
        self.assertTrue(check_distance + 100 >= km >= check_distance-100)

    def _check_readonly(self, url, code=status.HTTP_401_UNAUTHORIZED):
        res = self.client.get(url)
        self.assertTrue(status.is_success(res.status_code))
        res = self.client.post(url)
        self.assertTrue(res.status_code == code)

    def test_perm(self):
        self._check_readonly('/product/')
        self._check_readonly('/category/')
        self._check_readonly('/company/')
        self.registration('Test', '19960213Za')
        self._check_readonly('/product/', status.HTTP_400_BAD_REQUEST)
        self._check_readonly('/category/', status.HTTP_400_BAD_REQUEST)
        self._check_readonly('/company/', status.HTTP_400_BAD_REQUEST)


def get_products(id_: str):
    products = json.load(open(join(settings.BASE_DIR, 'core/fixtures/products.json')))
    return products[id_]


def get_companies():
    return json.load(open(join(settings.BASE_DIR, 'core/fixtures/companies.json')))


def side_effect_integration(url):
    if url == settings.COMPANIES_URL:
        return get_companies()

    company_id = re.search(r'.*([0-9]).*', url).group(1)
    return get_products(company_id)


class TestTaskIntegration(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for n in list(sys.modules.keys()):
            if n in 'utils':
                del sys.modules[n]

    def _check_db(self, company, company_id):
        prod = get_products(str(company_id))
        self.assertTrue(company.products.count() == len(prod))

    @patch('core.utils.request_json', side_effect=side_effect_integration)
    def test_integration(self, _):
        from core.tasks import integrate_companies
        integrate_companies(settings.COMPANIES_URL, settings.PRODUCTS_POSTFIX)

        companies = get_companies()
        self.assertTrue(len(companies) == Company.objects.count())
        self._check_db(Company.objects.first(), companies[0]['id'])
        self._check_db(Company.objects.last(), companies[1]['id'])


