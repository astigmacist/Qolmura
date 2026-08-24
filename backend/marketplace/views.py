from django.db.models import Count, Prefetch, Q
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .models import Artisan, Category, Product, ProductImage, SellerApplication
from .serializers import ArtisanSerializer, CategorySerializer, ProductSerializer, SellerApplicationSerializer


class ReadOnlyMarketplaceViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)


class CategoryViewSet(ReadOnlyMarketplaceViewSet):
    serializer_class = CategorySerializer
    ordering = ("sort_order", "name_kk")
    queryset = Category.objects.filter(is_active=True).annotate(
        product_count=Count(
            "products",
            filter=Q(products__status=Product.Status.ACTIVE, products__artisan__status=Artisan.Status.VERIFIED),
        )
    ).order_by("sort_order", "name_kk")
    lookup_field = "slug"


class ArtisanViewSet(ReadOnlyMarketplaceViewSet):
    serializer_class = ArtisanSerializer
    queryset = Artisan.objects.filter(status=Artisan.Status.VERIFIED)
    search_fields = ("shop_name", "city", "story_kk", "story_ru")
    lookup_field = "slug"


class ProductViewSet(ReadOnlyMarketplaceViewSet):
    serializer_class = ProductSerializer
    queryset = (
        Product.objects.filter(
            status=Product.Status.ACTIVE,
            artisan__status=Artisan.Status.VERIFIED,
            category__is_active=True,
        )
        .select_related("artisan", "category")
        .prefetch_related(Prefetch("images", queryset=ProductImage.objects.order_by("sort_order")))
    )
    filterset_fields = ("category__slug", "artisan__slug", "is_featured", "is_one_of_a_kind")
    search_fields = ("name_kk", "name_ru", "description_kk", "description_ru", "artisan__shop_name")
    ordering_fields = ("price", "created_at")
    lookup_field = "slug"


class SellerApplicationThrottle(AnonRateThrottle):
    scope = "seller_application"


class SellerApplicationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Public write-only endpoint: prospective sellers submit here, staff review in /admin/."""

    serializer_class = SellerApplicationSerializer
    queryset = SellerApplication.objects.all()
    permission_classes = (AllowAny,)
    throttle_classes = (SellerApplicationThrottle,)
