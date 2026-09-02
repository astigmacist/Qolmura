"""Official Qolmura Paris exhibition collection supplied on 2026-09-02.

Source: "Список ВЫСТАВКА ПАРИЖ 12.09.26 қолөнер шеберлері.docx".
Rows are split only when the source lists separately named or separately priced
products. Prices expressed as ranges are stored at their documented minimum.
"""


PARIS_STORY_KK = "Париж қаласының Төрн алаңындағы «Village kazakh» ұлттық мәдениет көрмесіне қатысушы қолөнер шебері."
PARIS_STORY_RU = "Мастер — участник выставки национальной культуры «Village kazakh» на площади Торн в Париже."

ARTISANS = {
    "dana_marlen": {
        "shop_name": "Дана Марлен",
        "slug": "dana-marlen",
        "city": "Сыр елі",
        "story_kk": f"Сән дизайнері. {PARIS_STORY_KK}",
        "story_ru": f"Дизайнер одежды. {PARIS_STORY_RU}",
    },
    "kasqyrbay": {
        "shop_name": "М. Қасқырбай",
        "slug": "m-kasqyrbay",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
    "aitmuratova": {
        "shop_name": "А. Айтмұратова",
        "slug": "a-aitmuratova",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
    "shorayev": {
        "shop_name": "Ж. Шораев",
        "slug": "zh-shorayev",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
    "abdiyeva": {
        "shop_name": "А. Абдиева",
        "slug": "a-abdiyeva",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
    "kenesbai": {
        "shop_name": "Д. Кеңесбай",
        "slug": "d-kenesbai",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
    "qudaibergenova": {
        "shop_name": "Г. Құдайбергенова",
        "slug": "g-qudaibergenova",
        "city": "Сыр елі",
        "story_kk": PARIS_STORY_KK,
        "story_ru": PARIS_STORY_RU,
    },
}


def _product(
    row,
    artisan,
    category,
    slug,
    name_kk,
    name_ru,
    source_note,
    price,
    stock,
    *,
    featured=False,
    price_is_from=False,
    materials_kk="",
    materials_ru="",
    dimensions_kk="",
    dimensions_ru="",
):
    return {
        "row": row,
        "artisan": artisan,
        "category": category,
        "slug": slug,
        "name_kk": name_kk,
        "name_ru": name_ru,
        "source_note": source_note,
        "price": price,
        "stock": stock,
        "featured": featured,
        "price_is_from": price_is_from,
        "materials_kk": materials_kk,
        "materials_ru": materials_ru,
        "dimensions_kk": dimensions_kk,
        "dimensions_ru": dimensions_ru,
    }


PRODUCTS = [
    _product("S1", "dana_marlen", "clothing", "dana-marlen-ethno-collection", "Этно стильдегі киім үлгілері", "Коллекция одежды в этностиле", "Бағасы: 65 000–75 000 теңге аралығы", 65000, 9, featured=True, price_is_from=True),
    _product("S2", "kasqyrbay", "bags-accessories", "leather-hand-travel-bags-kasqyrbay", "Былғары қол және жол сөмкелері", "Кожаные ручные и дорожные сумки", "Бағасы: 10 000–30 000 теңге аралығы", 10000, 4, featured=True, price_is_from=True, materials_kk="Былғары", materials_ru="Кожа"),
    _product("S3.1", "aitmuratova", "clothing", "beaded-velvet-kamzol-aitmuratova", "Моншақпен көмкерілген барқыт қамзол", "Бархатный камзол с бисером", "Бағасы: 70 000 теңге. Моншақтары жалтырап, ерекше үлгіде қолмен тігілген", 70000, 1, featured=True, materials_kk="Барқыт, моншақ", materials_ru="Бархат, бисер"),
    _product("S3.2", "aitmuratova", "clothing", "designer-velvet-kamzol-aitmuratova", "Дизайнерлік барқыт қамзол", "Дизайнерский бархатный камзол", "Бағасы: 40 000 теңге. Сапалы моншақтармен көмкерілген", 40000, 1, materials_kk="Барқыт, моншақ", materials_ru="Бархат, бисер"),
    _product("S3.3", "aitmuratova", "clothing", "collar-beldemshe-set-aitmuratova", "Жаға мен белдемше жиынтығы", "Комплект из воротника и белдемше", "Бағасы: 40 000 теңге", 40000, 1),
    _product("S3.4", "aitmuratova", "clothing", "long-kamzol-taqiya-aitmuratova", "Тақиялы ұзын қамзол", "Удлинённый камзол с такия", "Бағасы: 100 000 теңге. Шамамен 30 метр моншақ қолмен тігілген", 100000, 1, featured=True, materials_kk="Барқыт, моншақ", materials_ru="Бархат, бисер"),
    _product("S3.5", "aitmuratova", "clothing", "warm-long-kamzol-aitmuratova", "Астарлы ұзын жылы қамзол", "Удлинённый тёплый камзол", "Бағасы: 50 000 теңге. Астарланған және көктелген", 50000, 1, materials_kk="Барқыт, астар", materials_ru="Бархат, подкладка"),
    _product("S3.6", "aitmuratova", "clothing", "girls-beldemshe-aitmuratova", "Қыздарға арналған сәндік белдемше", "Декоративное белдемше для девушек", "Бағасы: 20 000 теңге. Киім сыртынан киіледі, моншақпен қолмен көмкерілген", 20000, 1, materials_kk="Барқыт, моншақ", materials_ru="Бархат, бисер"),
    _product("S3.7", "aitmuratova", "clothing", "ornamental-vest-aitmuratova", "Оюлы жилет", "Жилет с орнаментом", "Бағасы: 20 000 теңге", 20000, 1),
    _product("S4.1", "shorayev", "textiles", "aqboz-at-carpet", "«Ақбоз ат» кілемі", "Ковёр «Ақбоз ат»", "Акрил жібімен және тафтинг тапаншасымен тоқылған. Жалпы баға аралығы: 60 000–700 000 теңге", 60000, 1, featured=True, price_is_from=True, materials_kk="Акрил жібі", materials_ru="Акриловая пряжа", dimensions_kk="0,2 × 2,5 м", dimensions_ru="0,2 × 2,5 м"),
    _product("S4.2", "shorayev", "textiles", "qorqyt-carpet", "«Қорқыт» кілемі", "Ковёр «Коркыт»", "Акрил жібімен және тафтинг тапаншасымен тоқылған. Жалпы баға аралығы: 60 000–700 000 теңге", 60000, 1, price_is_from=True, materials_kk="Акрил жібі", materials_ru="Акриловая пряжа", dimensions_kk="0,80 × 0,60 м", dimensions_ru="0,80 × 0,60 м"),
    _product("S4.3", "shorayev", "textiles", "juyrik-tazy-carpet", "«Жүйрік тазы» кілемі", "Ковёр «Жүйрік тазы»", "Акрил жібімен және тафтинг тапаншасымен тоқылған. Жалпы баға аралығы: 60 000–700 000 теңге", 60000, 1, price_is_from=True, materials_kk="Акрил жібі", materials_ru="Акриловая пряжа", dimensions_kk="0,80 × 0,60 м", dimensions_ru="0,80 × 0,60 м"),
    _product("S4.4", "shorayev", "textiles", "asqaq-barys-carpet", "«Асқақ барыс» кілемі", "Ковёр «Асқақ барыс»", "Акрил жібімен және тафтинг тапаншасымен тоқылған. Жалпы баға аралығы: 60 000–700 000 теңге", 60000, 1, featured=True, price_is_from=True, materials_kk="Акрил жібі", materials_ru="Акриловая пряжа", dimensions_kk="1,80 × 1,20 м", dimensions_ru="1,80 × 1,20 м"),
    _product("S5", "abdiyeva", "clothing", "family-shapan-kamzol-abdiyeva", "Ерлерге, әйелдерге және балаларға арналған шапан мен қамзол", "Шапаны и камзолы для взрослых и детей", "Бағасы: 25 000–120 000 теңге аралығы", 25000, 4, featured=True, price_is_from=True, materials_kk="Таза кашемир, вельвет, жібек астар", materials_ru="Кашемир, вельвет, шёлковая подкладка"),
    _product("S6.1", "kenesbai", "textiles", "toytabak-pillows-kenesbai", "Тойтабақ және құрақ жастықтар", "Подушки «Тойтабақ» и лоскутные подушки", "Бағасы: 3 000–15 000 теңге аралығы", 3000, 2, price_is_from=True, materials_kk="Глянц велюр, дак, тылқы, джинс", materials_ru="Глянцевый велюр, дак, тылқы, деним", dimensions_kk="35 × 35 см", dimensions_ru="35 × 35 см"),
    _product("S6.2", "kenesbai", "bags-accessories", "zhauqazyn-bags-kenesbai", "«Жауқазын» сөмкелері мен косметика салғыштар", "Сумки «Жауқазын» и косметички", "Құрақпен тігілген сөмке, шопер және косметика салғыштар. Бағасы: 3 000–15 000 теңге аралығы", 3000, 2, featured=True, price_is_from=True, materials_kk="Глянц велюр, дак, тылқы, джинс", materials_ru="Глянцевый велюр, дак, тылқы, деним"),
    _product("S7", "qudaibergenova", "souvenirs", "childrens-toys-qudaibergenova", "Балаларға арналған жұмсақ ойыншықтар, жастықтар және тақиялар", "Мягкие игрушки, подушки и такия для детей", "Бағасы: 2 000–5 000 теңге аралығы", 2000, 2, featured=True, price_is_from=True, materials_kk="Глянц велюр, дак, тылқы", materials_ru="Глянцевый велюр, дак, тылқы"),
]
