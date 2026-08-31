from rest_framework import serializers
from .models import Artisan, Category, Product, ProductImage, SellerApplication


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name_kk", "name_ru", "slug", "image", "product_count")


class ArtisanSerializer(serializers.ModelSerializer):
    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = ("id", "shop_name", "slug", "story_kk", "story_ru", "city", "avatar", "cover", "rating", "is_verified")

    def get_is_verified(self, obj):
        return obj.status == Artisan.Status.VERIFIED


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt_kk", "alt_ru", "sort_order")


class ProductSerializer(serializers.ModelSerializer):
    artisan = ArtisanSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id", "name_kk", "name_ru", "slug", "description_kk", "description_ru",
            "materials_kk", "materials_ru", "dimensions_kk", "dimensions_ru", "care_kk", "care_ru",
            "production_time_days", "cover_url", "price", "price_is_from", "stock", "is_featured", "is_one_of_a_kind",
            "is_demo", "artisan", "category", "images", "created_at",
        )


class SellerApplicationSerializer(serializers.ModelSerializer):
    consent = serializers.BooleanField(write_only=True)

    class Meta:
        model = SellerApplication
        fields = (
            "id", "full_name", "email", "phone", "brand_name", "instagram", "city", "craft",
            "experience_years", "estimated_product_count", "message", "consent", "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        errors = {}
        phone_digits = "".join(character for character in attrs.get("phone", "") if character.isdigit())
        if len(phone_digits) < 10:
            errors["phone"] = "Телефон нөмірін толық көрсетіңіз."
        if not attrs.get("consent"):
            errors["consent"] = "Деректерді өңдеуге келісім қажет."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        validated_data.pop("consent", None)
        return super().create(validated_data)
