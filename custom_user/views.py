from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from .models import CustomUser
from .serializers import UserCreateSerializer
from .permissions import CurrentUserOrAdmin


class UserViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [CurrentUserOrAdmin]
