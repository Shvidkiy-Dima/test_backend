from django.db import models
from django.contrib.gis.db.models import PointField


class BaseCoreModel(models.Model):
    description = models.CharField(max_length=124, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Company(BaseCoreModel):
    coordinates = PointField(null=True, blank=True)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Product(BaseCoreModel):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.name} - {self.company}'

    class Meta:
        constraints = [models.UniqueConstraint(fields=['company', 'name'],
                                               name='uniq_in_company')]

