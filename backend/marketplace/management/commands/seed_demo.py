import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from marketplace.models import Artisan, Category, Product


CATALOG = [
    {
        "category": ("Керамика", "Керамика", "ceramics"),
        "artisan": ("Keruen Ceramics", "keruen-ceramics", "Алматы", "Керамика шеберханасы. Дәстүрлі оюды заманауи пішінмен үйлестіреді.", "Керамическая мастерская, соединяющая традиционный орнамент с современной формой."),
        "product": {
            "name_kk": "«Керуен» шай жиынтығы", "name_ru": "Чайный набор «Керуен»", "slug": "keruen-tea-set",
            "description_kk": "Ақшыл саздан қолмен жасалған шәйнек пен екі тостаған. Қоңыр ою әр бұйымға жеке салынады, сондықтан әр жиынтықтың өз мінезі бар.",
            "description_ru": "Чайник и две пиалы, вручную выполненные из светлой глины. Орнамент наносится отдельно на каждый предмет, поэтому каждый набор немного отличается.",
            "materials_kk": "Ақшыл саз, күңгірт глазурь", "materials_ru": "Светлая глина, матовая глазурь",
            "dimensions_kk": "Шәйнек 1,2 л · 2 тостаған 180 мл", "dimensions_ru": "Чайник 1,2 л · 2 пиалы по 180 мл",
            "care_kk": "Жұмсақ губкамен қолмен жуу ұсынылады.", "care_ru": "Рекомендуется ручная мойка мягкой губкой.",
            "production_time_days": 7, "cover_url": "http://127.0.0.1:5173/products/keruen-tea-set.webp", "price": "38500.00", "stock": 3, "is_featured": True, "is_one_of_a_kind": False,
        },
    },
    {
        "category": ("Киіз бұйымдар", "Изделия из войлока", "felt"),
        "artisan": ("Arqa Felt", "arqa-felt", "Қарағанды", "Табиғи жүннен сырмақ пен интерьерлік панно тігетін отбасылық шеберхана.", "Семейная мастерская интерьерных панно и сырмаков из натуральной шерсти."),
        "product": {
            "name_kk": "«Тұмар» киіз панносы", "name_ru": "Войлочное панно «Тумар»", "slug": "tumar-syrmaq",
            "description_kk": "Табиғи жүннен қолмен басылып, жапсырма әдісімен тігілген интерьерлік панно. Қошқармүйіз ырғағы үйге жылылық пен ұлттық мінез береді.",
            "description_ru": "Интерьерное панно из вручную свалянной натуральной шерсти с аппликацией. Ритм традиционного орнамента добавляет пространству тепло и характер.",
            "materials_kk": "Қой жүні, мақта жіп", "materials_ru": "Овечья шерсть, хлопковая нить",
            "dimensions_kk": "80 × 140 см", "dimensions_ru": "80 × 140 см",
            "care_kk": "Құрғақ тазалау. Тікелей күн сәулесінен қорғаңыз.", "care_ru": "Сухая чистка. Беречь от прямого солнечного света.",
            "production_time_days": 14, "cover_url": "http://127.0.0.1:5173/products/tumar-syrmaq.webp", "price": "89000.00", "stock": 1, "is_featured": True, "is_one_of_a_kind": True,
        },
    },
    {
        "category": ("Әшекейлер", "Украшения", "jewelry"),
        "artisan": ("Säule Silver", "saule-silver", "Астана", "Күміс пен табиғи тастан шағын сериялы әшекей жасайтын зергерлік шеберхана.", "Ювелирная мастерская малых серий из серебра и натурального камня."),
        "product": {
            "name_kk": "«Айым» күміс сырғасы", "name_ru": "Серебряные серьги «Айым»", "slug": "aiym-earrings",
            "description_kk": "Қолмен соғылған күмістен жасалған жеңіл сырға. Қызыл ақықтың жылы реңкі қараланған күмістің бедерін айқындайды.",
            "description_ru": "Лёгкие серьги из серебра ручной ковки. Тёплый сердолик подчёркивает рельеф чернёного металла.",
            "materials_kk": "925 сынамалы күміс, қызыл ақық", "materials_ru": "Серебро 925 пробы, сердолик",
            "dimensions_kk": "Ұзындығы 6 см · салмағы 11 г", "dimensions_ru": "Длина 6 см · вес 11 г",
            "care_kk": "Жұмсақ матада бөлек сақтаңыз, сумен жанастырмаңыз.", "care_ru": "Хранить отдельно в мягкой ткани, избегать контакта с водой.",
            "production_time_days": 5, "cover_url": "http://127.0.0.1:5173/products/aiym-earrings.webp", "price": "32000.00", "stock": 2, "is_featured": True, "is_one_of_a_kind": False,
        },
    },
    {
        "category": ("Былғары", "Кожа", "leather"),
        "artisan": ("Dala Leather", "dala-leather", "Шымкент", "Өсімдік иленген былғарыдан күнделікті қолдануға арналған бұйымдар жасайды.", "Создаёт повседневные изделия из кожи растительного дубления."),
        "product": {
            "name_kk": "«Көш» былғары сөмкесі", "name_ru": "Кожаная сумка «Көш»", "slug": "kosh-bag",
            "description_kk": "Шағын пішінді, қолмен тігілген иық сөмкесі. Былғары уақыт өте жұмсарып, өзіне тән табиғи патина қалыптастырады.",
            "description_ru": "Компактная сумка через плечо, полностью сшитая вручную. Со временем кожа становится мягче и приобретает индивидуальную патину.",
            "materials_kk": "Өсімдік иленген былғары, жүн бау, жез", "materials_ru": "Кожа растительного дубления, шерстяной ремень, латунь",
            "dimensions_kk": "23 × 18 × 7 см · бау 125 см", "dimensions_ru": "23 × 18 × 7 см · ремень 125 см",
            "care_kk": "Құрғақ шүберекпен сүртіңіз. Былғарыға арналған табиғи балауыз қолданыңыз.", "care_ru": "Протирать сухой тканью. Использовать натуральный воск для кожи.",
            "production_time_days": 9, "cover_url": "http://127.0.0.1:5173/products/kosh-bag.webp", "price": "54500.00", "stock": 4, "is_featured": False, "is_one_of_a_kind": False,
        },
    },
    {
        "category": ("Ағаш бұйымдар", "Изделия из дерева", "wood"),
        "artisan": ("Qarağash", "qaragash", "Алматы", "Жаңғақ пен қарағаштан ас үй және интерьер бұйымдарын қолмен ояды.", "Вручную вырезает предметы для дома из ореха и карагача."),
        "product": {
            "name_kk": "«Самал» жаңғақ тостағаны", "name_ru": "Ореховая чаша «Самал»", "slug": "samal-bowl",
            "description_kk": "Жаңғақ ағашының тұтас бөлігінен ойылған кең тостаған. Жиегіндегі өрнек қолмен қашалып, ортасы жезбен көмкерілген.",
            "description_ru": "Широкая чаша, вырезанная из цельного массива ореха. Орнамент по краю выполнен вручную, центр дополнен латунной вставкой.",
            "materials_kk": "Жаңғақ ағашы, жез, табиғи май", "materials_ru": "Орех, латунь, натуральное масло",
            "dimensions_kk": "Диаметрі 28 см · биіктігі 7 см", "dimensions_ru": "Диаметр 28 см · высота 7 см",
            "care_kk": "Суға салмаңыз. Қолмен жуып, бірден құрғатыңыз.", "care_ru": "Не замачивать. Мыть вручную и сразу вытирать насухо.",
            "production_time_days": 6, "cover_url": "http://127.0.0.1:5173/products/samal-bowl.webp", "price": "28500.00", "stock": 3, "is_featured": False, "is_one_of_a_kind": True,
        },
    },
    {
        "category": ("Ұлттық киім", "Национальная одежда", "clothing"),
        "artisan": ("Miras Atelier", "miras-atelier", "Түркістан", "Ұлттық кестені күнделікті киім пішініне бейімдейтін шағын ателье.", "Небольшое ателье, адаптирующее национальную вышивку к современной одежде."),
        "product": {
            "name_kk": "«Алма» барқыт камзолы", "name_ru": "Бархатный камзол «Алма»", "slug": "alma-vest",
            "description_kk": "Қою бордо барқыттан тігілген жеңсіз камзол. Алтын түсті кесте алдыңғы жиек пен етекке қолмен түсірілген.",
            "description_ru": "Женский камзол без рукавов из бархата глубокого бордового цвета. Золотистая вышивка вручную нанесена по бортам и краю.",
            "materials_kk": "Мақта барқыт, вискоза астар, кесте жіп", "materials_ru": "Хлопковый бархат, вискозная подкладка, нить для вышивки",
            "dimensions_kk": "M өлшемі · кеуде 92–96 см · ұзындығы 68 см", "dimensions_ru": "Размер M · грудь 92–96 см · длина 68 см",
            "care_kk": "Кәсіби құрғақ тазалау ұсынылады.", "care_ru": "Рекомендуется профессиональная сухая чистка.",
            "production_time_days": 12, "cover_url": "http://127.0.0.1:5173/products/alma-vest.webp", "price": "76000.00", "stock": 1, "is_featured": True, "is_one_of_a_kind": True,
        },
    },
]


class Command(BaseCommand):
    help = "Create a clearly marked demonstration catalog for local product development."

    def handle(self, *args, **options):
        public_site_url = os.getenv("QOLMURA_PUBLIC_SITE_URL", "http://127.0.0.1:5173").rstrip("/")
        User = get_user_model()
        for index, item in enumerate(CATALOG, start=1):
            name_kk, name_ru, category_slug = item["category"]
            category, _ = Category.objects.update_or_create(
                slug=category_slug,
                defaults={"name_kk": name_kk, "name_ru": name_ru, "is_active": True, "sort_order": index},
            )
            shop_name, artisan_slug, city, story_kk, story_ru = item["artisan"]
            user, _ = User.objects.get_or_create(username=f"demo-{artisan_slug}")
            artisan, _ = Artisan.objects.update_or_create(
                slug=artisan_slug,
                defaults={"owner": user, "shop_name": shop_name, "city": city, "story_kk": story_kk, "story_ru": story_ru, "status": Artisan.Status.VERIFIED, "rating": "5.00"},
            )
            defaults = {**item["product"], "artisan": artisan, "category": category, "status": Product.Status.ACTIVE, "is_demo": True}
            defaults["cover_url"] = defaults["cover_url"].replace("http://127.0.0.1:5173", public_site_url)
            slug = defaults.pop("slug")
            Product.objects.update_or_create(slug=slug, defaults=defaults)

        self.stdout.write(self.style.SUCCESS(f"Demo catalog ready: {len(CATALOG)} products."))
