import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from marketplace.catalog_2026 import ARTISANS as ASTANA_ARTISANS, CATEGORIES, PRODUCTS as ASTANA_PRODUCTS
from marketplace.catalog_paris_2026 import ARTISANS as PARIS_ARTISANS, PRODUCTS as PARIS_PRODUCTS
from marketplace.catalog_paris_september_2026 import ARTISANS as PARIS_SEPTEMBER_ARTISANS, PRODUCTS as PARIS_SEPTEMBER_PRODUCTS
from marketplace.models import Artisan, Category, Product


LEGACY_CATEGORY_SLUGS = {"ceramics", "felt", "jewelry", "leather", "wood", "clothing"}
ARTISANS = {**ASTANA_ARTISANS, **PARIS_ARTISANS, **PARIS_SEPTEMBER_ARTISANS}
PRODUCTS = [*ASTANA_PRODUCTS, *PARIS_PRODUCTS, *PARIS_SEPTEMBER_PRODUCTS]


def material_for(product):
    value = f"{product['name_kk']} {product['source_note']}".lower()
    if "кенеп" in value:
        return "Кенеп, майлы бояу", "Холст, масляные краски"
    if "күміс" in value:
        return "Күміс", "Серебро"
    if "ағаш" in value:
        return "Ағаш", "Дерево"
    if "шыны" in value:
        return "Шыны", "Стекло"
    if "күріш" in value:
        return "Күріш", "Рис"
    if "киіз" in value or "жүн" in value:
        return "Киіз, жүн", "Войлок, шерсть"
    return "", ""


class Command(BaseCommand):
    help = "Synchronize the official 2026 Qolmura catalog without creating mock data."

    @transaction.atomic
    def handle(self, *args, **options):
        public_site_url = os.getenv("QOLMURA_PUBLIC_SITE_URL", "http://127.0.0.1:5173").rstrip("/")
        User = get_user_model()

        categories = {}
        for sort_order, (slug, (name_kk, name_ru)) in enumerate(CATEGORIES.items(), start=1):
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    "name_kk": name_kk,
                    "name_ru": name_ru,
                    "is_active": True,
                    "sort_order": sort_order,
                },
            )
            categories[slug] = category

        artisans = {}
        for key, data in ARTISANS.items():
            username = f"catalog-{data['slug']}"
            user, _ = User.objects.get_or_create(username=username)
            artisan, _ = Artisan.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "owner": user,
                    "shop_name": data["shop_name"],
                    "city": data["city"],
                    "story_kk": data["story_kk"],
                    "story_ru": data["story_ru"],
                    "status": Artisan.Status.VERIFIED,
                    "rating": "5.00",
                },
            )
            artisans[key] = artisan

        official_slugs = set()
        for product in PRODUCTS:
            official_slugs.add(product["slug"])
            artisan = artisans[product["artisan"]]
            inferred_materials_kk, inferred_materials_ru = material_for(product)
            materials_kk = product.get("materials_kk") or inferred_materials_kk
            materials_ru = product.get("materials_ru") or inferred_materials_ru
            source_note = product["source_note"]
            catalog_product, created = Product.objects.get_or_create(
                slug=product["slug"],
                defaults={
                    "artisan": artisan,
                    "category": categories[product["category"]],
                    "name_kk": product["name_kk"],
                    "name_ru": product["name_ru"],
                    "description_kk": f"{product['name_kk']}. Автор: {artisan.shop_name}. Каталогтағы саны мен бағасы: {source_note}.",
                    "description_ru": f"{product['name_ru']}. Автор работы: {artisan.shop_name}. Количество и цена в исходном каталоге: {source_note}.",
                    "materials_kk": materials_kk,
                    "materials_ru": materials_ru,
                    "dimensions_kk": product.get("dimensions_kk", ""),
                    "dimensions_ru": product.get("dimensions_ru", ""),
                    "care_kk": "",
                    "care_ru": "",
                    "production_time_days": 0,
                    "cover_url": f"{public_site_url}/products/catalog/{product['slug']}.webp",
                    "price": product["price"],
                    "price_is_from": product["price_is_from"],
                    "stock": product["stock"],
                    "status": Product.Status.ACTIVE,
                    "is_featured": product["featured"],
                    "is_one_of_a_kind": product["stock"] == 1,
                    "is_demo": False,
                },
            )
            if not created and catalog_product.price_is_from != product["price_is_from"]:
                catalog_product.price_is_from = product["price_is_from"]
                catalog_product.save(update_fields=("price_is_from",))

        # Remove only the six known generated records. Admin-created products stay untouched.
        Product.objects.filter(is_demo=True).exclude(slug__in=official_slugs).delete()

        for category in Category.objects.filter(slug__in=LEGACY_CATEGORY_SLUGS):
            if not category.products.exists() and category.slug not in CATEGORIES:
                category.delete()

        for artisan in Artisan.objects.filter(owner__username__startswith="demo-"):
            if not artisan.products.exists():
                owner = artisan.owner
                artisan.delete()
                owner.delete()

        self.stdout.write(self.style.SUCCESS(f"Official catalog ready: {len(PRODUCTS)} products, {len(ARTISANS)} artisans."))
