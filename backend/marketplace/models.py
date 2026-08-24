from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name_kk = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name_kk")
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name_kk


class Artisan(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        SUSPENDED = "suspended", "Suspended"

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="artisan_profile")
    shop_name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    story_kk = models.TextField(blank=True)
    story_ru = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="artisans/avatars/", blank=True)
    cover = models.ImageField(upload_to="artisans/covers/", blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.shop_name


class Product(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEW = "review", "Under review"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    artisan = models.ForeignKey(Artisan, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name_kk = models.CharField(max_length=180)
    name_ru = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    description_kk = models.TextField()
    description_ru = models.TextField()
    materials_kk = models.CharField(max_length=240, blank=True)
    materials_ru = models.CharField(max_length=240, blank=True)
    dimensions_kk = models.CharField(max_length=180, blank=True)
    dimensions_ru = models.CharField(max_length=180, blank=True)
    care_kk = models.TextField(blank=True)
    care_ru = models.TextField(blank=True)
    production_time_days = models.PositiveSmallIntegerField(default=3)
    cover_url = models.URLField(blank=True, help_text="Remote image URL for the initial catalog; migrate to managed media in production.")
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_one_of_a_kind = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("-is_featured", "-created_at")
        indexes = [
            models.Index(fields=("status", "category", "-created_at")),
            models.Index(fields=("artisan", "status")),
        ]

    def __str__(self):
        return self.name_kk


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/%Y/%m/")
    alt_kk = models.CharField(max_length=180, blank=True)
    alt_ru = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "id")


class SellerApplication(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", "Жаңа"
        IN_REVIEW = "in_review", "Қаралуда"
        CONTACTED = "contacted", "Байланысқа шықты"
        APPROVED = "approved", "Қабылданды"
        REJECTED = "rejected", "Бас тартылды"

    full_name = models.CharField("Аты-жөні", max_length=160)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=32)
    brand_name = models.CharField("Шеберхана / бренд", max_length=160, blank=True)
    instagram = models.CharField("Instagram", max_length=120, blank=True)
    city = models.CharField("Қала", max_length=100)
    craft = models.CharField("Қолөнер түрі", max_length=200)
    experience_years = models.PositiveSmallIntegerField("Тәжірибе, жыл", null=True, blank=True)
    estimated_product_count = models.PositiveSmallIntegerField("Дайын бұйым саны", null=True, blank=True)
    message = models.TextField("Хабарлама", blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW, db_index=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Жауапты менеджер",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_seller_applications",
        limit_choices_to={"is_staff": True},
    )
    internal_notes = models.TextField("Ішкі ескертпе", blank=True)
    processed_at = models.DateTimeField("Өңделген уақыты", null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Шебер өтінімі"
        verbose_name_plural = "Шеберлер өтінімдері"

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"
