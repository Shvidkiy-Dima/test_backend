from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Product, Company, Category
from .serializers_mixin import DistanceSerializerMixin


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        fields = '__all__'
        model = Category


class CompanySerializer(DistanceSerializerMixin, serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        fields = '__all__'
        model = Company


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = CategorySerializer(instance.category).data
        ret['company'] = CategorySerializer(instance.company).data
        return ret

    class Meta:
        fields = '__all__'
        model = Product
        validators = [UniqueTogetherValidator(queryset=Product.objects.all(),
                                              fields=['company', 'name'])
                      ]