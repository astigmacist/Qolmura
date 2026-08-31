from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.utils import timezone

from .models import Artisan, Category, Product, ProductImage, SellerApplication


class QolmuraAdminSite(admin.AdminSite):
    site_header = "Qolmura басқару панелі"
    site_title = "Qolmura Admin"
    index_title = "Маркетплейсті басқару"
    index_template = "admin/qolmura_index.html"

    def index(self, request, extra_context=None):
        extra_context = {
            **(extra_context or {}),
            "qolmura_metrics": {
                "active_products": Product.objects.filter(status=Product.Status.ACTIVE).count(),
                "verified_artisans": Artisan.objects.filter(status=Artisan.Status.VERIFIED).count(),
                "open_applications": SellerApplication.objects.filter(
                    status__in=(SellerApplication.Status.NEW, SellerApplication.Status.IN_REVIEW)
                ).count(),
                "total_categories": Category.objects.filter(is_active=True).count(),
            },
        }
        return super().index(request, extra_context=extra_context)


qolmura_admin_site = QolmuraAdminSite(name="qolmura_admin")


@admin.register(Category, site=qolmura_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_kk", "name_ru", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    prepopulated_fields = {"slug": ("name_kk",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product, site=qolmura_admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_kk", "artisan", "category", "price", "price_is_from", "stock", "status", "is_featured", "is_demo")
    list_filter = ("status", "is_featured", "is_one_of_a_kind", "is_demo", "category")
    search_fields = ("name_kk", "name_ru", "artisan__shop_name")
    prepopulated_fields = {"slug": ("name_kk",)}
    inlines = (ProductImageInline,)
    list_editable = ("status", "is_featured")
    list_per_page = 30
    fieldsets = (
        ("Негізгі ақпарат", {"fields": ("artisan", "category", "status", "slug")}),
        ("Қазақша контент", {"fields": ("name_kk", "description_kk", "materials_kk", "dimensions_kk", "care_kk")}),
        ("Контент на русском", {"fields": ("name_ru", "description_ru", "materials_ru", "dimensions_ru", "care_ru")}),
        ("Сату", {"fields": ("price", "price_is_from", "stock", "production_time_days", "cover_url")}),
        ("Каталогта көрсету", {"fields": ("is_featured", "is_one_of_a_kind", "is_demo")}),
    )


@admin.register(Artisan, site=qolmura_admin_site)
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ("shop_name", "city", "status", "rating")
    list_filter = ("status", "city")
    search_fields = ("shop_name", "owner__email")
    prepopulated_fields = {"slug": ("shop_name",)}


@admin.action(description="Қаралуда деп белгілеу")
def mark_in_review(modeladmin, request, queryset):
    queryset.update(status=SellerApplication.Status.IN_REVIEW, assigned_to=request.user)


@admin.action(description="Байланысқа шықты деп белгілеу")
def mark_contacted(modeladmin, request, queryset):
    queryset.update(status=SellerApplication.Status.CONTACTED, assigned_to=request.user)


@admin.action(description="Өтінімді қабылдау")
def mark_approved(modeladmin, request, queryset):
    queryset.update(status=SellerApplication.Status.APPROVED, assigned_to=request.user, processed_at=timezone.now())


@admin.action(description="Өтінімнен бас тарту")
def mark_rejected(modeladmin, request, queryset):
    queryset.update(status=SellerApplication.Status.REJECTED, assigned_to=request.user, processed_at=timezone.now())


@admin.register(SellerApplication, site=qolmura_admin_site)
class SellerApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "brand_name", "city", "craft", "status", "assigned_to", "created_at")
    list_filter = ("status", "city", "craft", "created_at")
    list_editable = ("status",)
    search_fields = ("full_name", "email", "phone", "brand_name", "instagram", "city", "craft", "message")
    readonly_fields = ("created_at", "updated_at", "processed_at")
    date_hierarchy = "created_at"
    list_per_page = 30
    actions = (mark_in_review, mark_contacted, mark_approved, mark_rejected)
    fieldsets = (
        ("Өтініш беруші", {"fields": ("full_name", "email", "phone", "city")}),
        ("Шеберхана туралы", {"fields": ("brand_name", "instagram", "craft", "experience_years", "estimated_product_count", "message")}),
        ("Өтінімді өңдеу", {"fields": ("status", "assigned_to", "internal_notes", "processed_at")}),
        ("Жүйелік ақпарат", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if obj.status != SellerApplication.Status.NEW and obj.assigned_to_id is None:
            obj.assigned_to = request.user
        if obj.status in (SellerApplication.Status.APPROVED, SellerApplication.Status.REJECTED):
            obj.processed_at = obj.processed_at or timezone.now()
        else:
            obj.processed_at = None
        super().save_model(request, obj, form, change)


qolmura_admin_site.register(get_user_model(), UserAdmin)
qolmura_admin_site.register(Group, GroupAdmin)
