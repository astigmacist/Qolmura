from rest_framework.routers import DefaultRouter
from .views import ArtisanViewSet, CategoryViewSet, ProductViewSet, SellerApplicationViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("artisans", ArtisanViewSet, basename="artisan")
router.register("products", ProductViewSet, basename="product")
router.register("seller-applications", SellerApplicationViewSet, basename="seller-application")

urlpatterns = router.urls

