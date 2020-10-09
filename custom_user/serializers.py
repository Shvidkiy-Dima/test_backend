from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.authtoken.models import Token
from .models import CustomUser


class UserCreateSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        validate_password(password)
        return attrs

    def create(self, validated_data):
        new_user = CustomUser.objects.create_user(**validated_data)
        Token.objects.create(user=new_user)
        return new_user

    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'password', 'phone', 'email', 'id']
