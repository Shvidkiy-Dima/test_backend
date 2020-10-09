from django.urls import path
from rest_framework.authtoken import views
from .views import UserViewSet


urlpatterns = [
    path('get_token/', views.obtain_auth_token),
    path('registration/', UserViewSet.as_view(actions={'post': 'create'})),
    path('<int:pk>/', UserViewSet.as_view(actions={'get': 'retrieve'}))
]
