from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company, Product, Category
from .serializers import CompanySerializer, CategorySerializer, ProductSerializer
from .filters import CompanyFilter, ProductFilter
from .utils import required_params


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CompanyFilter

    @action(methods=['GET'], detail=False)
    @required_params(['coordinates'])
    def nearest(self, request):
        user_coordinates = [float(p) for p in request.query_params.get('coordinates').split(',')]
        qs = self.filter_queryset(self.get_queryset())
        companies = CompanySerializer(qs, coordinates=user_coordinates, many=True)
        return Response(companies.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ProductFilter
