from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Artisan, Category, Product, SellerApplication


class CatalogApiTests(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username="artisan")
        self.artisan = Artisan.objects.create(owner=user, shop_name="Test Studio", slug="test-studio", city="Almaty", status=Artisan.Status.VERIFIED)
        self.category = Category.objects.create(name_kk="Әшекей", name_ru="Украшение", slug="jewelry")
        Product.objects.create(
            artisan=self.artisan,
            category=self.category,
            name_kk="Тұмар",
            name_ru="Тумар",
            slug="tumar",
            description_kk="Сипаттама",
            description_ru="Описание",
            price="12000.00",
            status=Product.Status.ACTIVE,
        )

    def test_products_endpoint_returns_active_catalog(self):
        response = self.client.get(reverse("product-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], "tumar")

    def test_catalog_hides_products_from_unverified_artisans(self):
        pending_user = get_user_model().objects.create_user(username="pending-artisan")
        pending_artisan = Artisan.objects.create(
            owner=pending_user,
            shop_name="Pending Studio",
            slug="pending-studio",
            city="Astana",
            status=Artisan.Status.PENDING,
        )
        Product.objects.create(
            artisan=pending_artisan,
            category=self.category,
            name_kk="Жасырын бұйым",
            name_ru="Скрытое изделие",
            slug="hidden-product",
            description_kk="Сипаттама",
            description_ru="Описание",
            price="9000.00",
            status=Product.Status.ACTIVE,
        )

        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertNotIn("hidden-product", [item["slug"] for item in response.data["results"]])

    def test_category_count_includes_only_public_products(self):
        Product.objects.create(
            artisan=self.artisan,
            category=self.category,
            name_kk="Жоба",
            name_ru="Черновик",
            slug="draft-product",
            description_kk="Сипаттама",
            description_ru="Описание",
            price="5000.00",
            status=Product.Status.DRAFT,
        )

        response = self.client.get(reverse("category-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["product_count"], 1)


class SellerApplicationApiTests(APITestCase):
    payload = {
        "full_name": "Айым Серікқызы",
        "email": "aiym@example.com",
        "phone": "+7 701 123 45 67",
        "brand_name": "Aiyma Studio",
        "instagram": "@aiyma.studio",
        "city": "Алматы",
        "craft": "Киіз және кесте",
        "experience_years": 4,
        "estimated_product_count": 18,
        "message": "Qolmura-ға қосылғым келеді.",
        "consent": True,
    }

    def test_application_is_saved_for_admin_review(self):
        response = self.client.post(reverse("seller-application-list"), self.payload, format="json")

        self.assertEqual(response.status_code, 201)
        application = SellerApplication.objects.get()
        self.assertEqual(application.email, "aiym@example.com")
        self.assertEqual(application.status, SellerApplication.Status.NEW)
        self.assertNotIn("status", response.data)
        self.assertNotIn("internal_notes", response.data)

    def test_application_requires_complete_contact_details_and_consent(self):
        invalid_payload = {**self.payload, "phone": "123", "consent": False}

        response = self.client.post(reverse("seller-application-list"), invalid_payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data)
        self.assertIn("consent", response.data)

    def test_application_requires_valid_email(self):
        response = self.client.post(
            reverse("seller-application-list"),
            {**self.payload, "email": "not-an-email"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_public_cannot_list_applications(self):
        response = self.client.get(reverse("seller-application-list"))

        self.assertEqual(response.status_code, 405)


class AdminPanelTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="operations",
            email="operations@qolmura.kz",
            password="test-only-password",
        )
        SellerApplication.objects.create(
            full_name="Мадина Асан",
            email="madina@example.com",
            phone="+7 701 555 44 33",
            city="Астана",
            craft="Керамика",
        )
        self.client.force_login(self.admin_user)

    def test_branded_dashboard_and_application_queue_are_available(self):
        dashboard_response = self.client.get(reverse("qolmura_admin:index"))
        application_response = self.client.get(
            reverse("qolmura_admin:marketplace_sellerapplication_changelist")
        )

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, "Маркетплейстің жағдайы")
        self.assertContains(dashboard_response, "Жаңа және қаралуда")
        self.assertEqual(application_response.status_code, 200)
        self.assertContains(application_response, "Мадина Асан")
