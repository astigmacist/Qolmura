import { useEffect, useMemo, useState, type FormEvent } from "react"
import { ArrowLeft, ArrowRight, Moon, Search, SlidersHorizontal, Sparkles, Sun } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { MarketplaceProductCard } from "@/components/MarketplaceProductCard"
import { getCategories, getProducts, type Category, type PaginatedProducts } from "@/lib/api"
import { useScrolled } from "@/lib/useScrolled"

type Language = "kk" | "ru"
type Theme = "light" | "dark"

const copy = {
  kk: {
    back: "Басты бет",
    search: "Бұйым немесе шеберді іздеу",
    eyebrow: "Qolmura коллекциясы",
    title: "Қазақстан шеберлерінің қолөнері",
    lead: "Түпнұсқа бұйымдарды санат, шебер және баға бойынша табыңыз.",
    all: "Барлығы",
    sort: "Сұрыптау",
    newest: "Алдымен жаңалары",
    low: "Бағасы: төменнен",
    high: "Бағасы: жоғарыдан",
    found: "бұйым табылды",
    loading: "Каталог жүктелуде",
    emptyTitle: "Алғашқы коллекция дайындалып жатыр",
    emptyText: "Qolmura командасы шеберлер мен түпнұсқа бұйымдарды іріктеп жатыр. Ресми жаңалықтарды Instagram парақшасынан көріңіз.",
    emptySearchTitle: "Сұраныс бойынша бұйым табылмады",
    emptySearchText: "Басқа атауды қолданып көріңіз немесе барлық санатқа оралыңыз.",
    reset: "Сүзгілерді тазарту",
    instagram: "Instagram-ға өту",
    errorTitle: "Каталогқа қосылу мүмкін болмады",
    errorText: "Бірнеше минуттан кейін қайта көріңіз.",
    retry: "Қайта көру",
    previous: "Алдыңғы",
    next: "Келесі",
    page: "Бет",
    one: "Бірегей дана",
    verified: "Тексерілген шебер",
    favorite: "Таңдаулыға қосу",
    removeFavorite: "Таңдаулыдан алып тастау",
    open: "Толығырақ",
    from: "бастап",
  },
  ru: {
    back: "На главную",
    search: "Найти изделие или мастера",
    eyebrow: "Коллекция Qolmura",
    title: "Ремесло мастеров Казахстана",
    lead: "Находите подлинные изделия по категории, мастеру и цене.",
    all: "Все",
    sort: "Сортировка",
    newest: "Сначала новые",
    low: "Цена: по возрастанию",
    high: "Цена: по убыванию",
    found: "изделий найдено",
    loading: "Загружаем каталог",
    emptyTitle: "Первая коллекция готовится",
    emptyText: "Команда Qolmura отбирает мастеров и подлинные изделия. Следите за официальными новостями в Instagram.",
    emptySearchTitle: "По вашему запросу ничего не найдено",
    emptySearchText: "Попробуйте другое название или вернитесь ко всем категориям.",
    reset: "Сбросить фильтры",
    instagram: "Перейти в Instagram",
    errorTitle: "Не удалось подключиться к каталогу",
    errorText: "Попробуйте ещё раз через несколько минут.",
    retry: "Повторить",
    previous: "Назад",
    next: "Дальше",
    page: "Страница",
    one: "Уникальный экземпляр",
    verified: "Проверенный мастер",
    favorite: "Добавить в избранное",
    removeFavorite: "Убрать из избранного",
    open: "Подробнее",
    from: "от",
  },
} as const

export function CatalogPage({ language, theme, onLanguageChange, onThemeChange }: {
  language: Language
  theme: Theme
  onLanguageChange: () => void
  onThemeChange: () => void
}) {
  const initialSearch = useMemo(() => new URLSearchParams(window.location.search).get("search") ?? "", [])
  const [query, setQuery] = useState(initialSearch)
  const [search, setSearch] = useState(initialSearch)
  const [category, setCategory] = useState("")
  const [ordering, setOrdering] = useState("-created_at")
  const [page, setPage] = useState(1)
  const [categories, setCategories] = useState<Category[]>([])
  const [catalog, setCatalog] = useState<PaginatedProducts | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const t = copy[language]
  const scrolled = useScrolled()

  useEffect(() => {
    document.title = language === "kk" ? "Қолөнер каталогы — Qolmura" : "Каталог ремесла — Qolmura"
  }, [language])

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    setError(false)
    const params = new URLSearchParams()
    if (search) params.set("search", search)
    if (category) params.set("category__slug", category)
    if (ordering) params.set("ordering", ordering)
    if (page > 1) params.set("page", String(page))

    window.history.replaceState(null, "", `/catalog${params.toString() ? `?${params}` : ""}`)
    Promise.all([getCategories(controller.signal), getProducts(params, controller.signal)])
      .then(([categoryData, productData]) => {
        setCategories(categoryData)
        setCatalog(productData)
      })
      .catch((requestError: unknown) => {
        if (requestError instanceof DOMException && requestError.name === "AbortError") return
        setError(true)
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false)
      })
    return () => controller.abort()
  }, [category, ordering, page, search])

  function submitSearch(event: FormEvent) {
    event.preventDefault()
    setPage(1)
    setSearch(query.trim())
  }

  function resetFilters() {
    setQuery("")
    setSearch("")
    setCategory("")
    setOrdering("-created_at")
    setPage(1)
  }

  const hasFilters = Boolean(search || category)
  const totalPages = Math.max(1, Math.ceil((catalog?.count ?? 0) / 24))

  function changePage(nextPage: number) {
    setPage(nextPage)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  return (
    <div className="catalog-page">
      <header className="catalog-header" data-scrolled={scrolled}>
        <div className="container catalog-header-grid">
          <a href="/" className="brand" aria-label="Qolmura"><img src="/qolmura-mark.png" alt="" /><span>QOLMURA</span></a>
          <form className="catalog-search" onSubmit={submitSearch} role="search">
            <Search aria-hidden="true" />
            <Input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t.search} aria-label={t.search} />
            <Button type="submit" size="icon" aria-label={t.search}><ArrowRight /></Button>
          </form>
          <div className="catalog-actions">
            <Button variant="ghost" size="sm" onClick={onLanguageChange}>{language === "kk" ? "ҚАЗ" : "RU"}</Button>
            <Button variant="ghost" size="icon" onClick={onThemeChange} aria-label={theme === "light" ? "Тёмная тема" : "Светлая тема"}>{theme === "light" ? <Moon /> : <Sun />}</Button>
          </div>
        </div>
      </header>

      <main>
        <section className="catalog-hero">
          <div className="container">
            <a href="/" className="catalog-back"><ArrowLeft />{t.back}</a>
            <div className="catalog-heading">
              <div><span>{t.eyebrow}</span><h1>{t.title}</h1></div>
              <p>{t.lead}</p>
            </div>
          </div>
        </section>

        <section className="catalog-body">
          <div className="container">
            <div className="catalog-toolbar">
              <div className="category-filters" aria-label="Категории">
                <button className={!category ? "active" : ""} onClick={() => { setCategory(""); setPage(1) }}>{t.all}</button>
                {categories.map((item) => <button key={item.slug} className={category === item.slug ? "active" : ""} onClick={() => { setCategory(item.slug); setPage(1) }}>{language === "kk" ? item.name_kk : item.name_ru}<span>{item.product_count}</span></button>)}
              </div>
              <label className="sort-control"><SlidersHorizontal /><span>{t.sort}</span><select value={ordering} onChange={(event) => { setOrdering(event.target.value); setPage(1) }}><option value="-created_at">{t.newest}</option><option value="price">{t.low}</option><option value="-price">{t.high}</option></select></label>
            </div>

            {!loading && !error && <p className="catalog-count">{catalog?.count ?? 0} {t.found}</p>}

            {loading && <div className="catalog-status"><div className="catalog-loader" /><p>{t.loading}</p></div>}
            {error && <div className="catalog-status"><div className="empty-seal"><img src="/qolmura-mark.png" alt="" /></div><h2>{t.errorTitle}</h2><p>{t.errorText}</p><Button onClick={() => window.location.reload()}>{t.retry}</Button></div>}
            {!loading && !error && catalog?.results.length === 0 && <div className="catalog-status"><div className="empty-seal"><img src="/qolmura-mark.png" alt="" /></div><span className="empty-kicker"><Sparkles />QOLMURA</span><h2>{hasFilters ? t.emptySearchTitle : t.emptyTitle}</h2><p>{hasFilters ? t.emptySearchText : t.emptyText}</p><div className="empty-actions">{hasFilters && <Button variant="outline" onClick={resetFilters}>{t.reset}</Button>}<Button asChild><a href="https://www.instagram.com/qolmura.kz/" target="_blank" rel="noreferrer">{t.instagram}<ArrowRight /></a></Button></div></div>}

            {!loading && !error && Boolean(catalog?.results.length) && (
              <div className="product-grid">
                {catalog?.results.map((product) => (
                  <MarketplaceProductCard key={product.id} product={product} language={language} labels={{
                    one: t.one,
                    verified: t.verified,
                    favorite: t.favorite,
                    removeFavorite: t.removeFavorite,
                    open: t.open,
                    from: t.from,
                  }} />
                ))}
              </div>
            )}
            {!loading && !error && Boolean(catalog?.results.length) && totalPages > 1 && (
              <nav className="catalog-pagination" aria-label={t.page}>
                <Button variant="outline" disabled={page <= 1} onClick={() => changePage(page - 1)}><ArrowLeft />{t.previous}</Button>
                <span>{t.page} <strong>{page}</strong> / {totalPages}</span>
                <Button variant="outline" disabled={page >= totalPages} onClick={() => changePage(page + 1)}>{t.next}<ArrowRight /></Button>
              </nav>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}
