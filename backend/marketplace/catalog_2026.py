"""Official Qolmura exhibition catalog supplied on 2026-08-31.

The source is the table in "Список ВЫСТАВКА Астана - 08.07.2026.docx".
Keep the original Kazakh quantity/price note intact: it is the only source of
commercial details supplied for these works.
"""

CATEGORIES = {
    "clothing": ("Ұлттық киім", "Национальная одежда"),
    "textiles": ("Тоқыма және киіз", "Текстиль и войлок"),
    "bags-accessories": ("Сөмкелер мен аксессуарлар", "Сумки и аксессуары"),
    "visual-art": ("Бейнелеу өнері", "Изобразительное искусство"),
    "wood": ("Ағаш бұйымдары", "Изделия из дерева"),
    "musical-instruments": ("Музыкалық аспаптар", "Музыкальные инструменты"),
    "jewelry": ("Зергерлік бұйымдар", "Ювелирные изделия"),
    "souvenirs": ("Кәдесыйлар", "Сувениры"),
}


ARTISANS = {
    "ilyasova": {
        "shop_name": "Ильясова Карлыгаш Серикбаевна",
        "slug": "karlygash-ilyasova",
        "city": "Қызылорда",
        "story_kk": "Қазақстан Қолөнершілер одағының мүшесі, қолөнер шебері. Қызылорда қаласында тұрады, жеке кәсіпкер.",
        "story_ru": "Член Союза ремесленников Казахстана, мастер прикладного искусства. Живёт в Кызылорде, индивидуальный предприниматель.",
    },
    "toishybayev": {
        "shop_name": "Дәулетбек Тойшыбаев",
        "slug": "dauletbek-toishybayev",
        "city": "Қызылорда",
        "story_kk": "Қазақстан Суретшілер одағының мүшесі, суретші және қолөнер шебері. Қызылорда қаласында тұрады, жеке кәсіпкер.",
        "story_ru": "Член Союза художников Казахстана, художник и мастер прикладного искусства. Живёт в Кызылорде, индивидуальный предприниматель.",
    },
    "makhanbet": {
        "shop_name": "Жәнібек Маханбет",
        "slug": "zhanibek-makhanbet",
        "city": "Сырдария ауданы",
        "story_kk": "Қазақстан Суретшілер одағының мүшесі, ағаш өңдеу шебері. Сырдария ауданында тұрады, зейнеткер.",
        "story_ru": "Член Союза художников Казахстана, мастер художественной обработки дерева. Живёт в Сырдарьинском районе, пенсионер.",
    },
    "dilmanov": {
        "shop_name": "Біржан Ділманов",
        "slug": "birzhan-dilmanov",
        "city": "Қызылорда",
        "story_kk": "Ұлттық музыкалық аспаптар шебері. Қызылорда қаласында тұрады, жеке кәсіпкер.",
        "story_ru": "Мастер национальных музыкальных инструментов. Живёт в Кызылорде, индивидуальный предприниматель.",
    },
    "kalzhanova": {
        "shop_name": "Майя Қалжанова",
        "slug": "maya-kalzhanova",
        "city": "Шиелі ауданы",
        "story_kk": "Қазақстан Қолөнершілер одағының мүшесі, басқұр тоқу шебері. Шиелі ауданында тұрады, аудандық оқушылар үйінде қоғамдық қызметкер.",
        "story_ru": "Член Союза ремесленников Казахстана, мастер ткачества баскура. Живёт в Шиелийском районе, работает в районном доме школьников.",
    },
    "mautova": {
        "shop_name": "Ұлмекен Мауытова",
        "slug": "ulmeken-mautova",
        "city": "Жаңақорған ауданы",
        "story_kk": "Қазақстан Суретшілер одағының мүшесі, суретші және қолөнер шебері. Жаңақорған ауданында тұрады, зейнеткер.",
        "story_ru": "Член Союза художников Казахстана, художник и мастер прикладного искусства. Живёт в Жанакорганском районе, пенсионер.",
    },
    "sadykov": {
        "shop_name": "Садықов Пахрадин",
        "slug": "pakhradin-sadykov",
        "city": "Қызылорда облысы",
        "story_kk": "Ағаш өңдеу шебері.",
        "story_ru": "Мастер художественной обработки дерева.",
    },
    "zhaqypov": {
        "shop_name": "Бегзат Жакипов",
        "slug": "begzat-zhakipov",
        "city": "Қызылорда",
        "story_kk": "Қазақстан Қолөнершілер одағының мүшесі, зергер. Қызылорда қаласында тұрады, жеке кәсіпкер.",
        "story_ru": "Член Союза ремесленников Казахстана, ювелир. Живёт в Кызылорде, индивидуальный предприниматель.",
    },
}


def _product(row, artisan, category, slug, name_kk, name_ru, source_note, price, stock, *, featured=False, price_is_from=False):
    return {
        "row": row,
        "artisan": artisan,
        "category": category,
        "slug": slug,
        "name_kk": name_kk,
        "name_ru": name_ru,
        "source_note": source_note,
        "price": price,
        "price_is_from": price_is_from,
        "stock": stock,
        "featured": featured,
    }


PRODUCTS = [
    _product(2, "ilyasova", "clothing", "kimeshek", "Кимешек", "Кимешек", "5 дана * 15 000 теңгеден", 15000, 5, featured=True),
    _product(3, "ilyasova", "clothing", "taqiya", "Тақия", "Такия", "20 дана * 15 000 теңгеден", 15000, 20, featured=True),
    _product(4, "ilyasova", "clothing", "ethno-cap", "Этнокепка", "Этнокепка", "10 дана * 15 000 теңгеден", 15000, 10),
    _product(5, "ilyasova", "textiles", "tufted-carpet", "Түкті кілем", "Ворсовый ковёр", "Өлшемі 1,50 * 0,70 — 1 дана * 400 000 теңге; өлшемі 0,50 * 0,50 — 2 дана * 30 000 теңгеден; өлшемі 0,40 * 0,40 — 2 дана * 25 000 теңгеден", 25000, 5, featured=True, price_is_from=True),
    _product(6, "ilyasova", "textiles", "tuskiiz-wall-carpet", "Түс киіз", "Настенный ковёр тускииз", "Өлшемі 1,60 * 3,00 — 2 дана * 500 000 теңгеден", 500000, 2),
    _product(7, "ilyasova", "textiles", "textile-wall-panel", "Панно", "Текстильное панно", "Өлшемі 1,30 * 0,70 — 1 дана * 45 000 теңге; өлшемі 1,40 * 0,70 — 1 дана * 45 000 теңге", 45000, 2),
    _product(8, "ilyasova", "bags-accessories", "ethno-bags", "Этносөмкелер", "Этносумки", "45 дана * 5 000, 12 000, 30 000 теңге аралығы", 5000, 45, featured=True, price_is_from=True),
    _product(9, "ilyasova", "textiles", "felt-footwear", "Киізден жасалған аяқ киім", "Обувь из войлока", "10 дана * 18 000 теңгеден", 18000, 10),
    _product(10, "ilyasova", "souvenirs", "souvenir-set", "Кәдесый", "Сувенир", "20 дана * 3 000 теңгеден", 3000, 20),
    _product(11, "ilyasova", "bags-accessories", "patchwork-korzhyn", "Құрақ қоржын", "Лоскутный коржын", "5 дана * 20 000 теңгеден", 20000, 5),
    _product(12, "ilyasova", "textiles", "bridal-trousseau", "Қыз жасауы", "Приданое невесты", "2 жиынтық * 500 000 теңгеден", 500000, 2),
    _product(13, "ilyasova", "clothing", "national-clothing", "Ұлттық киімдер", "Национальная одежда", "10 дана * 15 000–50 000 теңге аралығы", 15000, 10, price_is_from=True),
    _product(15, "toishybayev", "visual-art", "glass-engravings", "Соққылы нүктелік шыны гравюрасы", "Ударно-точечная гравюра по стеклу", "25 дана * 300 000–600 000 теңге аралығы", 300000, 25, featured=True, price_is_from=True),
    _product(16, "toishybayev", "textiles", "art-carpets", "Кілемдер", "Ковры", "5 дана * 500 000 теңгеден", 500000, 5),
    _product(17, "toishybayev", "visual-art", "rice-paintings", "Күріштен салынған картиналар", "Картины из риса", "6 дана * 200 000 теңгеден бастап", 200000, 6, price_is_from=True),
    _product(18, "makhanbet", "wood", "wooden-artworks-zhanibek", "Ағаштан жасалған қолөнер бұйымдары", "Авторские изделия из дерева", "40–50 дана жұмыс * 3 000–150 000 теңге аралығы", 3000, 40, featured=True, price_is_from=True),
    _product(19, "dilmanov", "musical-instruments", "national-musical-instruments", "Ұлттық музыкалық аспаптар", "Национальные музыкальные инструменты", "20–30 дана аралығы * 200 000 теңгеден басталады", 200000, 20, featured=True, price_is_from=True),
    _product(20, "kalzhanova", "textiles", "alasha", "Алаша", "Алаша", "1 дана * 150 000 теңге, ені 150 см, ұзындығы 250 см", 150000, 1),
    _product(21, "kalzhanova", "textiles", "tus-alasha", "Түс алаша", "Цветная алаша", "1 дана * 200 000 теңге, ені 2 м, ұзындығы 3 м", 200000, 1),
    _product(22, "kalzhanova", "textiles", "uzik-bau", "Үзік баулар", "Тканые ленты для юрты", "3 дана * 75 000 теңгеден, ені 19 см, ұзындығы 8 м", 75000, 3),
    _product(23, "kalzhanova", "textiles", "aq-bau", "Ақ бау", "Белая тканая лента", "1 дана * 75 000 теңге, ені 21 см, ұзындығы 8 м", 75000, 1),
    _product(24, "kalzhanova", "bags-accessories", "korzhyn-ayakqap-keseqap", "Қоржын, аяққап, кесеқап", "Коржын, аяккап и чехол для пиал", "Қоржын — 1 дана * 85 000 теңге; аяққап — 1 дана * 60 000 теңге; кесеқап — 1 дана * 40 000 теңге", 40000, 3, price_is_from=True),
    _product(25, "kalzhanova", "textiles", "uyq-bau", "Уық баулар (шашақты)", "Ленты для уыков с кистями", "7 дана * 7 000 теңгеден, ұзындығы 150 см", 7000, 7),
    _product(26, "kalzhanova", "bags-accessories", "woven-belts", "Белдіктер", "Тканые пояса", "5 дана * 5 000 теңгеден, ұзындығы 150 см", 5000, 5),
    _product(27, "kalzhanova", "bags-accessories", "tumarsha", "Тұмарша", "Тумарша", "5 дана * 15 000 теңгеден, ені 25 см, ұзындығы 85 см", 15000, 5),
    _product(28, "kalzhanova", "bags-accessories", "national-handbags", "Ұлттық нақыштағы қол сөмкелер", "Сумки с национальным орнаментом", "6 дана * 20 000 теңгеден, ені 30 см, ұзындығы 30 см", 20000, 6, featured=True),
    _product(29, "kalzhanova", "souvenirs", "uy-tumar", "Үй тұмар (шашақты)", "Домашний тумар с кистями", "Жұбымен 4 дана * 10 000 теңгеден", 10000, 4),
    _product(30, "kalzhanova", "bags-accessories", "tassel-keychains", "Брелок шашақтар", "Брелоки-кисти", "30 дана * 1 500 теңгеден", 1500, 30),
    _product(31, "mautova", "visual-art", "altyn-qaqpa-felt", "«Алтын қақпа», киізден жасалған", "«Золотые ворота», войлок", "Өлшемі 100 × 64 см, 1 дана * 70 000 теңге", 70000, 1, featured=True),
    _product(32, "mautova", "visual-art", "samgau-felt", "«Самғау», киізден жасалған", "«Самгау», войлок", "Өлшемі 150 × 86 см, 1 дана * 70 000 теңге", 70000, 1),
    _product(33, "mautova", "visual-art", "dancer-birches-felt", "«Биші қайыңдар», киізден жасалған", "«Танцующие берёзы», войлок", "1 дана * 50 000 теңге", 50000, 1),
    _product(34, "mautova", "visual-art", "night-melody-felt", "«Түнгі сарын», киізден жасалған", "«Ночной мотив», войлок", "1 дана * 70 000 теңге", 70000, 1),
    _product(35, "mautova", "visual-art", "barshyn-sulu-felt", "«Баршын сұлу», киізден жасалған", "«Баршын сулу», войлок", "1 дана * 30 000 теңге", 30000, 1),
    _product(36, "mautova", "visual-art", "duet-painting", "«Дуэт» картинасы", "Картина «Дуэт»", "Кенеп, майлы бояу; 1 дана * 50 000 теңге", 50000, 1),
    _product(37, "mautova", "visual-art", "happiness-painting", "«Бақыт құшағында» картинасы", "Картина «В объятиях счастья»", "Кенеп, майлы бояу; 1 дана * 50 000 теңге", 50000, 1),
    _product(38, "mautova", "visual-art", "golden-yard-painting", "«Алтын аула» картинасы", "Картина «Золотой двор»", "Кенеп, майлы бояу; 1 дана * 20 000 теңге", 20000, 1),
    _product(39, "mautova", "visual-art", "truth-in-the-well-painting", "«Шыңыраудағы шындық» картинасы", "Картина «Истина в колодце»", "Кенеп, майлы бояу; 1 дана * 50 000 теңге", 50000, 1),
    _product(40, "mautova", "visual-art", "life-painting", "«Тіршілік» картинасы", "Картина «Жизнь»", "Кенеп, майлы бояу; 1 дана * 50 000 теңге", 50000, 1),
    _product(41, "mautova", "textiles", "felt-prayer-mat", "Жайнамаз, киізден жасалған", "Молитвенный коврик из войлока", "1 дана * 10 000 теңге", 10000, 1),
    _product(42, "mautova", "clothing", "felt-vests", "Киізден басылған нымшалар", "Валяные жилеты", "3 дана * 8 000–15 000 теңге аралығы", 8000, 3, price_is_from=True),
    _product(43, "mautova", "textiles", "felt-seat-cushions", "Киізден басылған орындыққа арналған көрпешелер", "Войлочные подушки для стульев", "2 дана * 5 000 теңгеден", 5000, 2),
    _product(44, "mautova", "souvenirs", "felt-boxes", "Жүннен басылған шкатулкалар", "Валяные шкатулки", "3 дана * 5 000 теңгеден", 5000, 3),
    _product(45, "mautova", "textiles", "felt-slippers-mautova", "Жүннен басылған бәпіштер", "Валяные тапочки", "5 дана * 5 000–10 000 теңге аралығы", 5000, 5, price_is_from=True),
    _product(46, "mautova", "souvenirs", "felt-apples", "Жүннен дайындалған кәдесый алмалар", "Сувенирные яблоки из войлока", "6 дана * 4 000 теңге", 4000, 6),
    _product(47, "mautova", "souvenirs", "felt-jewelry-box", "Киіз қобдиша", "Войлочная шкатулка", "1 дана * 8 000 теңге", 8000, 1),
    _product(49, "sadykov", "wood", "wooden-artworks-sadykov", "Ағаштан жасалған қолөнер бұйымдары", "Авторские изделия из дерева", "50-ден астам жұмыс * 75 000–380 000 теңге аралығы", 75000, 50, featured=True, price_is_from=True),
    _product(50, "zhaqypov", "musical-instruments", "sazsyrnay", "Сазсырнай", "Сазсырнай", "10 дана * 5 000 теңгеден", 5000, 10),
    _product(51, "zhaqypov", "musical-instruments", "qylqobyz", "Қылқобыз", "Кылкобыз", "1 дана * 600 000 теңге", 600000, 1, featured=True),
    _product(52, "zhaqypov", "jewelry", "creative-talisman", "Креативті бойтұмар", "Авторский талисман", "1 дана * 600 000 теңге", 600000, 1),
    _product(53, "zhaqypov", "jewelry", "silver-bracelets", "Күміс және күміс жалатылған білезіктер", "Серебряные и посеребрённые браслеты", "1 дана * 150 000 теңге; 15 дана * 10 000 теңгеден", 10000, 16, featured=True, price_is_from=True),
    _product(54, "zhaqypov", "jewelry", "silver-rings", "Күміс жүзіктер", "Серебряные кольца", "2 дана * 75 000 теңгеден; 10 дана * 45 000 теңгеден", 45000, 12, price_is_from=True),
    _product(55, "zhaqypov", "bags-accessories", "kise-belt", "Кісе белдік", "Пояс кисе", "1 дана * 300 000 теңге", 300000, 1),
    _product(56, "zhaqypov", "musical-instruments", "shanqobyz", "Шаңқобыз", "Шанкобыз", "8 дана * 30 000 теңгеден", 30000, 8),
    _product(57, "zhaqypov", "bags-accessories", "qamshy", "Қамшы", "Камча", "5 дана * 30 000 теңгеден", 30000, 5),
    _product(58, "zhaqypov", "musical-instruments", "dauylpaz", "Дауылпаз", "Дауылпаз", "1 дана * 80 000 теңге", 80000, 1),
]
