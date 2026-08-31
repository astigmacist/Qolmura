"""Official Qolmura Paris exhibition collection supplied on 2026-08-31.

Source: "Список ВЫСТАВКА ПАРИЖ 30.04.26 қолөнер шеберлері (1).docx".
Grouped table rows are split into individual marketplace products whenever the
source provides a separate name, quantity and price.
"""


ARTISANS = {
    "shamshieva": {
        "shop_name": "Шамшиева Ақбота Сеилханқызы",
        "slug": "akbota-shamshieva",
        "city": "Қазақстан",
        "story_kk": "Париж қаласының Төрн алаңында өткен «Village kazakh» ұлттық мәдениет көрмесіне қатысқан қолөнер шебері.",
        "story_ru": "Мастер прикладного искусства, участница выставки национальной культуры «Village kazakh» на площади Торн в Париже.",
    },
}


def _product(row, category, slug, name_kk, name_ru, source_note, price, stock, *, featured=False, price_is_from=False):
    return {
        "row": row,
        "artisan": "shamshieva",
        "category": category,
        "slug": slug,
        "name_kk": name_kk,
        "name_ru": name_ru,
        "source_note": source_note,
        "price": price,
        "stock": stock,
        "featured": featured,
        "price_is_from": price_is_from,
    }


PRODUCTS = [
    _product("P1", "souvenirs", "omir-iirimderi-talisman", "«Өмір иірімдері» тұмары", "Талисман «Спирали жизни»", "Өлшемі 32 × 24 × 4 см; 5 дана * 45 000 теңгеден", 45000, 5, featured=True),
    _product("P2", "clothing", "ethno-collars-akbota", "Этно жағалықтар", "Этноворотники", "30 дана * 8 000–15 000 теңге аралығы", 8000, 30, featured=True, price_is_from=True),
    _product("P3.1", "clothing", "modern-shapan-akbota", "Заманауи этно шапан", "Современный этношапан", "Шапан — 1 дана * 50 000 теңге", 50000, 1),
    _product("P3.2", "clothing", "patchwork-shapan-akbota", "Құрақ шапан", "Лоскутный шапан", "Құрақ шапан — 1 дана * 35 000 теңге", 35000, 1, featured=True),
    _product("P3.3", "clothing", "hooded-shapan-akbota", "Капюшонды шапан", "Шапан с капюшоном", "Копюшонды шапан — 1 дана * 80 000 теңге", 80000, 1),
    _product("P3.4", "clothing", "coat-suit-akbota", "Костюм-пальто", "Костюм-пальто", "Костюм-пальто — 1 дана * 75 000 теңге", 75000, 1),
    _product("P3.5", "clothing", "light-shapan-akbota", "Жұқа шапан", "Лёгкий шапан", "Жұқа шапан (ұзын, қысқа) — 2 дана * 20 000–30 000 теңге аралығы", 20000, 2, price_is_from=True),
    _product("P3.6", "clothing", "ethno-vests-akbota", "Этно жилеттер", "Этножилеты", "Жилет — 13 дана * 15 000–50 000 теңге аралығы", 15000, 13, featured=True, price_is_from=True),
    _product("P3.7", "clothing", "beldemshe-baska-akbota", "Белдемше-баска", "Пояс-баска", "Белдемше (баска) — 2 дана * 10 000–15 000 теңге аралығы", 10000, 2, price_is_from=True),
    _product("P3.8", "clothing", "beldemshe-skirt-akbota", "Белдемше-юбка", "Этноюбка", "Белдемше (юбка) — 1 дана * 15 000 теңге", 15000, 1),
    _product("P4", "bags-accessories", "shopper-bags-akbota", "Шопер сөмке", "Сумка-шопер", "3 дана * 9 000 теңгеден", 9000, 3, featured=True),
    _product("P5", "souvenirs", "asyk-chess-akbota", "Асық-шахмат ойыны", "Шахматы с асыками", "1 дана * 40 000 теңге", 40000, 1),
    _product("P6", "clothing", "felt-berets-akbota", "Жүннен басылған этно береткалар", "Валяные этнобереты", "10 дана * 15 000 теңгеден", 15000, 10),
    _product("P7", "textiles", "chair-cushions-akbota", "Орындықтарға арналған төсегіштер", "Подушки для стульев", "2 дана * 15 000 теңгеден", 15000, 2),
    _product("P8.1", "jewelry", "sautoirs-akbota", "Этно сотуарлар", "Этносотуары", "Сотуар — 10 дана * 12 000 теңгеден", 12000, 10, featured=True),
    _product("P8.2", "jewelry", "bracelets-akbota", "Этно білезіктер", "Этнобраслеты", "Білезік — 40 дана * 5 000 теңгеден", 5000, 40),
    _product("P8.3", "jewelry", "earrings-akbota", "Этно сырғалар", "Этносерьги", "Сырға — 30 дана * 6 000 теңгеден", 6000, 30),
    _product("P8.4", "jewelry", "necklaces-akbota", "Этно алқалар", "Этноожерелья", "Алқа — 40 дана * 5 000–15 000 теңге аралығы", 5000, 40, price_is_from=True),
    _product("P8.5", "souvenirs", "keychains-akbota", "Этно брелоктар", "Этнобрелоки", "Брелок — 10 дана * 7 000 теңгеден", 7000, 10),
    _product("P8.6", "jewelry", "pins-akbota", "Этно түйреуіштер", "Этнобулавки", "Түйреуіш — 10 дана * 5 000 теңгеден", 5000, 10),
    _product("P8.7", "jewelry", "brooches-akbota", "Этно брошкалар", "Этноброши", "Брошка — 30 дана * 4 000 теңгеден", 4000, 30),
    _product("P9", "textiles", "baypaq-akbota", "Байпақ", "Валяные байпаки", "6 дана * 17 000 теңге", 17000, 6, featured=True),
]
