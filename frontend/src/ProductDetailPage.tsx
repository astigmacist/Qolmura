import { useEffect, useState } from "react"
import { ArrowLeft, Check, Clock, Heart, MapPin, Moon, PackageCheck, ShieldCheck, ShoppingBag, Sparkles, Sun, Truck } from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Button } from "@/components/ui/button"
import { getProduct, resolveMediaUrl, type Product } from "@/lib/api"
import { useScrolled } from "@/lib/useScrolled"

type Language = "kk" | "ru"
type Theme = "light" | "dark"

const copy = {
  kk: {
    catalog: "Каталогқа оралу", demo: "Демо коллекция", unique: "Бірегей дана", verified: "Тексерілген шебер",
    material: "Материал", size: "Өлшем", making: "Дайындау мерзімі", days: "күн",
    add: "Себетке қосу", added: "Себетке қосылды", favorite: "Таңдаулыға қосу", removeFavorite: "Таңдаулыдан алып тастау",
    stock: "Қоймада бар", last: "Соңғы дана", delivery: "Қазақстан бойынша жеткізу", deliveryText: "2–5 жұмыс күні, құны мекенжай бойынша есептеледі.",
    authenticity: "Түпнұсқалық кепілі", authenticityText: "Әр бұйым тексерілген шеберден тікелей ұсынылады.",
    returns: "Қолдау", returnsText: "Тапсырыс бойынша Qolmura командасы көмектеседі.",
    description: "Бұйым туралы", care: "Күтім", shipping: "Жеткізу және қаптама",
    shippingText: "Бұйым қорғаныш қаптамасына салынып, Қазақстан бойынша трек-нөмірімен жіберіледі.",
    master: "Шебер туралы", masterProducts: "Шебердің бұйымдарын көру", loading: "Бұйым жүктелуде",
    error: "Бұйым табылмады", errorText: "Каталогқа оралып, басқа бұйымды таңдаңыз.",
    disclosure: "Бұл карточка интерфейсті көрсетуге арналған демонстрациялық коллекцияға жатады. Баға, шебер және сипаттамалар — мок деректер.",
    cart: "Себет",
  },
  ru: {
    catalog: "Вернуться в каталог", demo: "Демо-коллекция", unique: "Уникальный экземпляр", verified: "Проверенный мастер",
    material: "Материал", size: "Размер", making: "Срок изготовления", days: "дней",
    add: "Добавить в корзину", added: "Добавлено в корзину", favorite: "Добавить в избранное", removeFavorite: "Убрать из избранного",
    stock: "В наличии", last: "Последний экземпляр", delivery: "Доставка по Казахстану", deliveryText: "2–5 рабочих дней, стоимость рассчитывается по адресу.",
    authenticity: "Гарантия подлинности", authenticityText: "Каждое изделие поступает напрямую от проверенного мастера.",
    returns: "Поддержка", returnsText: "Команда Qolmura помогает по вопросам заказа.",
    description: "Об изделии", care: "Уход", shipping: "Доставка и упаковка",
    shippingText: "Изделие упаковывается в защитную упаковку и отправляется по Казахстану с трек-номером.",
    master: "О мастере", masterProducts: "Посмотреть изделия мастера", loading: "Загружаем изделие",
    error: "Изделие не найдено", errorText: "Вернитесь в каталог и выберите другое изделие.",
    disclosure: "Эта карточка относится к демонстрационной коллекции для проверки интерфейса. Цена, мастер и характеристики — мок-данные.",
    cart: "Корзина",
  },
} as const

function readCart() {
  try { return JSON.parse(localStorage.getItem("qolmura-cart") ?? "{}") as Record<string, number> } catch { return {} }
}

function readFavorites() {
  try { return JSON.parse(localStorage.getItem("qolmura-favorites") ?? "[]") as string[] } catch { return [] }
}

export function ProductDetailPage({ slug, language, theme, onLanguageChange, onThemeChange }: {
  slug: string
  language: Language
  theme: Theme
  onLanguageChange: () => void
  onThemeChange: () => void
}) {
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [favorite, setFavorite] = useState(() => readFavorites().includes(slug))
  const [added, setAdded] = useState(false)
  const [cartCount, setCartCount] = useState(() => Object.values(readCart()).reduce((sum, quantity) => sum + quantity, 0))
  const t = copy[language]
  const scrolled = useScrolled()

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    getProduct(slug, controller.signal)
      .then(setProduct)
      .catch((requestError: unknown) => {
        if (requestError instanceof DOMException && requestError.name === "AbortError") return
        setError(true)
      })
      .finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [slug])

  function toggleFavorite() {
    const next = !favorite
    const values = new Set(readFavorites())
    if (next) values.add(slug); else values.delete(slug)
    localStorage.setItem("qolmura-favorites", JSON.stringify([...values]))
    setFavorite(next)
  }

  function addToCart() {
    const cart = readCart()
    cart[slug] = (cart[slug] ?? 0) + 1
    localStorage.setItem("qolmura-cart", JSON.stringify(cart))
    setCartCount(Object.values(cart).reduce((sum, quantity) => sum + quantity, 0))
    setAdded(true)
    window.setTimeout(() => setAdded(false), 1800)
  }

  const name = product ? (language === "kk" ? product.name_kk : product.name_ru) : "Qolmura"
  const description = product ? (language === "kk" ? product.description_kk : product.description_ru) : ""
  const materials = product ? (language === "kk" ? product.materials_kk : product.materials_ru) : ""
  const dimensions = product ? (language === "kk" ? product.dimensions_kk : product.dimensions_ru) : ""
  const care = product ? (language === "kk" ? product.care_kk : product.care_ru) : ""

  useEffect(() => {
    document.title = product ? `${name} — Qolmura` : "Qolmura"
  }, [name, product])

  return <div className="detail-page">
    <header className="detail-header" data-scrolled={scrolled}><div className="container detail-header-grid">
      <a href="/" className="brand" aria-label="Qolmura"><img src="/qolmura-mark.png" alt="" /><span>QOLMURA</span></a>
      <a href="/catalog" className="detail-back"><ArrowLeft />{t.catalog}</a>
      <div className="detail-actions"><Button variant="ghost" size="sm" onClick={onLanguageChange}>{language === "kk" ? "ҚАЗ" : "RU"}</Button><Button variant="ghost" size="icon" onClick={onThemeChange} aria-label={theme === "light" ? "Тёмная тема" : "Светлая тема"}>{theme === "light" ? <Moon /> : <Sun />}</Button><div className="cart-indicator"><ShoppingBag /><span>{cartCount}</span><i>{t.cart}</i></div></div>
    </div></header>

    <main>
      {loading && <div className="detail-status"><div className="catalog-loader" /><p>{t.loading}</p></div>}
      {!loading && (error || !product) && <div className="detail-status"><div className="empty-seal"><img src="/qolmura-mark.png" alt="" /></div><h1>{t.error}</h1><p>{t.errorText}</p><Button asChild><a href="/catalog">{t.catalog}</a></Button></div>}
      {!loading && product && <>
        <section className="product-detail-section"><div className="container product-detail-grid">
          <div className="detail-media detail-media-zoom"><img src={resolveMediaUrl(product.cover_url)} alt={name} /><div className="detail-media-badges">{product.is_demo && <span><Sparkles />{t.demo}</span>}{product.is_one_of_a_kind && <span>{t.unique}</span>}</div><span className="detail-image-index">01 / 01</span></div>
          <div className="detail-info">
            <div className="detail-kicker"><span>{language === "kk" ? product.category.name_kk : product.category.name_ru}</span><span>QOLMURA</span></div>
            <h1>{name}</h1>
            <div className="detail-artisan"><div className="artisan-avatar">{product.artisan.shop_name.slice(0, 1)}</div><div><strong>{product.artisan.shop_name}</strong><span><MapPin />{product.artisan.city} · {t.verified}</span></div></div>
            <div className="detail-price"><strong>{new Intl.NumberFormat(language === "kk" ? "kk-KZ" : "ru-KZ").format(Number(product.price))} ₸</strong><span><Check />{product.stock === 1 ? t.last : t.stock}</span></div>
            <p className="detail-description">{description}</p>
            <dl className="detail-specs"><div><dt>{t.material}</dt><dd>{materials}</dd></div><div><dt>{t.size}</dt><dd>{dimensions}</dd></div><div><dt>{t.making}</dt><dd>{product.production_time_days} {t.days}</dd></div></dl>
            <div className="detail-buttons"><Button size="lg" onClick={addToCart}>{added ? <Check /> : <ShoppingBag />}{added ? t.added : t.add}</Button><Button size="lg" variant="outline" onClick={toggleFavorite} aria-label={favorite ? t.removeFavorite : t.favorite}><Heart fill={favorite ? "currentColor" : "none"} />{favorite ? t.removeFavorite : t.favorite}</Button></div>
            <div className="detail-assurances"><div><Truck /><span><strong>{t.delivery}</strong>{t.deliveryText}</span></div><div><ShieldCheck /><span><strong>{t.authenticity}</strong>{t.authenticityText}</span></div><div><PackageCheck /><span><strong>{t.returns}</strong>{t.returnsText}</span></div></div>
            <Accordion type="single" collapsible className="detail-accordion"><AccordionItem value="description"><AccordionTrigger>{t.description}</AccordionTrigger><AccordionContent>{description}</AccordionContent></AccordionItem><AccordionItem value="care"><AccordionTrigger>{t.care}</AccordionTrigger><AccordionContent>{care}</AccordionContent></AccordionItem><AccordionItem value="shipping"><AccordionTrigger>{t.shipping}</AccordionTrigger><AccordionContent>{t.shippingText}</AccordionContent></AccordionItem></Accordion>
          </div>
        </div></section>

        <section className="master-section"><div className="container master-grid"><div className="master-label"><span>{t.master}</span><div className="master-monogram"><i>{product.artisan.shop_name.slice(0, 1)}</i></div></div><div className="master-copy"><span>{product.artisan.city}</span><h2>{product.artisan.shop_name}</h2><p>{language === "kk" ? product.artisan.story_kk : product.artisan.story_ru}</p><Button asChild variant="outline"><a href={`/catalog?search=${encodeURIComponent(product.artisan.shop_name)}`}>{t.masterProducts}<ArrowLeft className="rotate-180" /></a></Button></div></div></section>
        {product.is_demo && <aside className="demo-disclosure"><div className="container"><Sparkles /><p>{t.disclosure}</p></div></aside>}
      </>}
    </main>
  </div>
}
