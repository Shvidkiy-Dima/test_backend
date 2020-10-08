from django.contrib.gis import admin
from .models import Company, Product, Category


admin.site.register(Company, admin.GeoModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
