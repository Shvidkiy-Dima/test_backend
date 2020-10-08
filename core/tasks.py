import logging
from contextlib import contextmanager
from django.conf import settings
from celery import shared_task
from .models import Company, Category
from .utils import request_json

logger = logging.getLogger('integration_task')


@contextmanager
def integration_logging():
    logger.info(f'Start integration. Start fetching data from {settings.COMPANIES_URL}')
    try:
        yield
    except Exception as e:
        logger.error(f'Integration error: {e}')
    else:
        logger.info('Integration was successful')


@shared_task
def integrate():
    with integration_logging():
        integrate_companies(settings.COMPANIES_URL, settings.PRODUCTS_POSTFIX)


def integrate_companies(company_api_url, product_prefix):
    companies = request_json(company_api_url)
    for company, id in [(c, c.pop('id')) for c in companies]:
        company, b = Company.objects.update_or_create(name=company['name'], defaults=company)
        products = request_json(f'{company_api_url}{id}{product_prefix}')
        will_del = company.products.exclude(name__in=[p['name'] for p in products])

        logger.info(f'Get {"New" if b else ""} company {company}. Catch '
                    f'{len(products)} products. {will_del.count()} products will be deleted')

        will_del.delete()
        integrate_products(company, products)


def integrate_products(company, products):
    logger.info(f'Populate {company} products')

    for product, category, _ in [(p, p.pop('category'), p.pop('id')) for p in products]:
        category.pop('id')
        product['category'], _ = Category.objects.get_or_create(**category, defaults=category)
        product, b = company.products.update_or_create(name=product['name'], defaults=product)

        logger.info(f'{"Add" if b else "Update"} product {product} in company {company}')
