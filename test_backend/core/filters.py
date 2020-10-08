from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter
from .models import Company, Product


class ActiveFilterMixin(FilterSet):
    is_active = BooleanFilter()


class CompanyFilter(ActiveFilterMixin):

    class Meta:
        model = Company
        fields = ['is_active']


class ProductFilter(ActiveFilterMixin):
    company = CharFilter(field_name='company__name')
    category = CharFilter(field_name='category__name')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['is_active', 'company', 'name', 'category']
