from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, CompanyViewSet, CategoryViewSet

router = SimpleRouter()

router.register('product', viewset=ProductViewSet)
router.register('company', viewset=CompanyViewSet)
router.register('category', viewset=CategoryViewSet)

urlpatterns = router.urls
