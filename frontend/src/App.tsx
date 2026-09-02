import { useEffect, useRef, useState, type FormEvent } from "react"
import {
  ArrowRight,
  Check,
  Gem,
  HeartHandshake,
  Instagram,
  LayoutGrid,
  Menu,
  Moon,
  PackageCheck,
  Search,
  ShieldCheck,
  Sparkles,
  Store,
  Sun,
  Truck,
  UserRound,
  X,
} from "lucide-react"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Sheet, SheetContent, SheetDescription, SheetTitle } from "@/components/ui/sheet"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { MarketplaceProductCard } from "@/components/MarketplaceProductCard"
import { CatalogPage } from "@/CatalogPage"
import { ProductDetailPage } from "@/ProductDetailPage"
import { getProducts, submitSellerApplication, type Product } from "@/lib/api"
import { useReveal } from "@/lib/useReveal"
import { useScrolled } from "@/lib/useScrolled"

type Language = "kk" | "ru"
type Theme = "light" | "dark"

const content = {
  kk: {
    catalog: "Каталог",
    about: "Qolmura туралы",
    forArtisans: "Шеберлерге",
    faq: "Сұрақтар",
    search: "Бұйым немесе шеберді іздеу",
    searchTitle: "Qolmura каталогы дайындалып жатыр",
    searchText: "Қазір біз алғашқы шеберлер мен түпнұсқа бұйымдарды іріктеп жатырмыз. Іске қосылғанда іздеу осы жерден жұмыс істейді.",
    searchAction: "Instagram-ға өту",
    login: "Кіру",
    seller: "Сатушы болу",
    eyebrow: "Қазақстан қолөнерінің жаңа кеңістігі",
    title: "Шебердің қолынан — сіздің үйіңізге.",
    lead: "Qolmura Қазақстан шеберлерінің бірегей туындыларын жинайды. Әр бұйым — қол еңбегі, ұлттық мұра және автордың өз тарихы.",
    primary: "Qolmura-мен танысу",
    secondary: "Шебер ретінде қосылу",
    official: "Qolmura ресми парақшасы",
    officialBio: "Қолөнер тауарларының маркетплейсы",
    officialText: "Шеберлерден ерекше және сапалы бұйымдар. Қазақи стильдегі қолөнерді қолда!",
    whyLabel: "Неге Qolmura?",
    whyTitle: "Қолөнерге арналған жеке орта",
    whyLead: "Qolmura шеберлердің еңбегін әділ бағалап, олардың бірегей туындыларын көпшілікке қолжетімді етуді мақсат етеді.",
    buyerTab: "Сатып алушыға",
    artisanTab: "Шеберге",
    buyerTitle: "Бірегей бұйымды сеніммен табыңыз",
    buyerText: "Ұлттық стильдегі, сапалы және түпнұсқа қолөнерді бір жерден таңдау. Бұйымның авторын және оның тарихын жақынырақ тану.",
    artisanTitle: "Еңбегіңізді жаңа аудиторияға танытыңыз",
    artisanText: "Өнімді онлайн ұсынуға, тұрақты сатып алушы табуға және өз брендіңізді дамытуға арналған түсінікті платформа.",
    valuesTitle: "Qolmura не өзгертеді",
    valuesLead: "Шебер мен сатып алушы арасындағы жолды қысқартамыз.",
    stepOne: "Шеберлерді біріктіреміз",
    stepOneText: "Қала мен ауылдағы қолөнершілерге өз жұмысын таныстыруға ортақ кеңістік береміз.",
    stepTwo: "Түпнұсқалықты алға қоямыз",
    stepTwoText: "Авторлық өнімді жаппай өндірілген тауардан ажырататын сенімді орта құрамыз.",
    stepThree: "Сатып алуды жеңілдетеміз",
    stepThreeText: "Іздеу, төлем және жеткізуді бір түсінікті жолға біріктіруді жоспарлаймыз.",
    statement: "Qolmura — қолөнершілер мен олардың туындыларын сүйетіндерге арналған ерекше әлем.",
    statementSource: "Qolmura манифесі",
    artisanCta: "Өз қолыңыздан шыққан бұйымдар көпшілікке лайық.",
    artisanCtaText: "Алғашқы Qolmura шеберлерінің қатарына қосылуға өтінім қалдырыңыз.",
    apply: "Өтінім қалдыру",
    faqTitle: "Жиі қойылатын сұрақтар",
    q1: "Qolmura деген не?",
    a1: "Qolmura — Қазақстан қолөнер шеберлері мен бірегей бұйым іздейтін сатып алушыларды байланыстыратын маркетплейс жобасы.",
    q2: "Каталог қашан ашылады?",
    a2: "Каталогта Астана және Париж көрмелерінің 94 нақты бұйымы бар. Жаңа шеберлер туралы жаңалықтар @qolmura.kz парақшасында жарияланады.",
    q3: "Шебер қалай қосыла алады?",
    a3: "Қазір Instagram немесе байланыс нөмірі арқылы Qolmura командасына хабарласуға болады. Шеберлер үшін тіркелу және тауар орналастыру жолы платформада бөлек қарастырылады.",
    contact: "Байланыс",
    mission: "Қазақстан қолөнерін заманауи форматта танытатын маркетплейс.",
    menu: "Мәзір",
    close: "Жабу",
    themeLight: "Жарық тақырып",
    themeDark: "Қараңғы тақырып",
    featuredEyebrow: "ҰСЫНЫЛҒАН БҰЙЫМДАР",
    featuredTitle: "Соңғы қосылған бұйымдар",
    featuredLead: "Шеберлер қолымен жасалған ерекше туындылардың бір бөлігі.",
    featuredCta: "Каталогты толық қарау",
    uniqueBadge: "Бірегей дана",
    verifiedBadge: "Тексерілген шебер",
    favorite: "Таңдаулыға қосу",
    removeFavorite: "Таңдаулыдан алып тастау",
    openProduct: "Толығырақ",
    categoryFallback: "Qolmura",
    stat1: "қолмен жасалған",
    stat2: "қолөнер санаты",
    stat3: "күнде жеткізу дайын",
    stat4: "әр бұйым — бірегей дана",
    formName: "Аты-жөніңіз",
    formEmail: "Email",
    formPhone: "Телефон",
    formBrand: "Шеберхана немесе бренд атауы",
    formInstagram: "Instagram (міндетті емес)",
    formCity: "Қала",
    formCraft: "Қолөнер түрі",
    formExperience: "Тәжірибе, жыл",
    formProductCount: "Сатуға дайын бұйым саны",
    formMessage: "Хабарлама (міндетті емес)",
    formContactSection: "Байланыс деректері",
    formWorkshopSection: "Шеберхана туралы",
    formConsent: "Деректерімді Qolmura командасының өтінімді өңдеуі үшін пайдалануға келісемін.",
    formSubmit: "Өтінімді жіберу",
    formSending: "Жіберілуде…",
    formSuccess: "Рахмет! Өтініміңіз қабылданды, жақын арада хабарласамыз.",
    formError: "Жіберу мүмкін болмады. Қайта көріңіз немесе Instagram арқылы жазыңыз.",
    formOr: "Немесе тікелей хабарласыңыз",
  },
  ru: {
    catalog: "Каталог",
    about: "О Qolmura",
    forArtisans: "Мастерам",
    faq: "Вопросы",
    search: "Найти изделие или мастера",
    searchTitle: "Каталог Qolmura готовится к запуску",
    searchText: "Сейчас мы отбираем первых мастеров и подлинные изделия. После запуска поиск будет работать здесь.",
    searchAction: "Перейти в Instagram",
    login: "Войти",
    seller: "Стать продавцом",
    eyebrow: "Новое пространство ремесла Казахстана",
    title: "Из рук мастера — в ваш дом.",
    lead: "Qolmura объединяет уникальные работы мастеров Казахстана. Каждое изделие — ручной труд, национальное наследие и личная история автора.",
    primary: "Познакомиться с Qolmura",
    secondary: "Присоединиться как мастер",
    official: "Официальная страница Qolmura",
    officialBio: "Маркетплейс изделий ручной работы",
    officialText: "Особенные и качественные изделия от мастеров. Поддерживайте ремесло в казахском стиле!",
    whyLabel: "Почему Qolmura?",
    whyTitle: "Отдельная среда для ремесла",
    whyLead: "Qolmura стремится справедливо оценивать труд мастеров и делать их уникальные работы доступными широкой аудитории.",
    buyerTab: "Покупателю",
    artisanTab: "Мастеру",
    buyerTitle: "Находите уникальные вещи с доверием",
    buyerText: "Выбирайте качественное и подлинное ремесло в национальном стиле в одном месте. Узнавайте автора изделия и его историю.",
    artisanTitle: "Покажите свой труд новой аудитории",
    artisanText: "Понятная платформа для онлайн-продаж, поиска постоянных покупателей и развития собственного бренда.",
    valuesTitle: "Что меняет Qolmura",
    valuesLead: "Сокращаем путь между мастером и покупателем.",
    stepOne: "Объединяем мастеров",
    stepOneText: "Создаём общее пространство, где ремесленники из городов и сёл смогут показать свою работу.",
    stepTwo: "Ставим подлинность на первое место",
    stepTwoText: "Формируем доверенную среду, отличающую авторское изделие от массового товара.",
    stepThree: "Упрощаем покупку",
    stepThreeText: "Планируем объединить поиск, оплату и доставку в одном понятном процессе.",
    statement: "Qolmura — особый мир для ремесленников и тех, кто любит их творения.",
    statementSource: "Манифест Qolmura",
    artisanCta: "Изделия, созданные вашими руками, достойны большой аудитории.",
    artisanCtaText: "Оставьте заявку, чтобы войти в число первых мастеров Qolmura.",
    apply: "Оставить заявку",
    faqTitle: "Частые вопросы",
    q1: "Что такое Qolmura?",
    a1: "Qolmura — проект маркетплейса, который связывает мастеров Казахстана с покупателями, ищущими уникальные изделия.",
    q2: "Когда откроется каталог?",
    a2: "В каталоге уже представлены 94 реальные работы из коллекций выставок в Астане и Париже. Новости о новых мастерах публикуются на странице @qolmura.kz.",
    q3: "Как мастеру присоединиться?",
    a3: "Сейчас можно связаться с командой Qolmura через Instagram или по контактному номеру. Регистрация и размещение товаров для мастеров будут отдельной частью платформы.",
    contact: "Контакты",
    mission: "Маркетплейс, представляющий ремесло Казахстана в современном формате.",
    menu: "Меню",
    close: "Закрыть",
    themeLight: "Светлая тема",
    featuredEyebrow: "РЕКОМЕНДУЕМ",
    featuredTitle: "Недавно добавленные изделия",
    featuredLead: "Часть уникальных работ, созданных руками мастеров.",
    featuredCta: "Смотреть весь каталог",
    uniqueBadge: "Уникальный экземпляр",
    verifiedBadge: "Проверенный мастер",
    favorite: "Добавить в избранное",
    removeFavorite: "Убрать из избранного",
    openProduct: "Подробнее",
    categoryFallback: "Qolmura",
    stat1: "ручная работа",
    stat2: "категории ремесла",
    stat3: "дня на доставку",
    stat4: "каждое изделие уникально",
    formName: "Ваше имя",
    formEmail: "Email",
    formPhone: "Телефон",
    formBrand: "Название мастерской или бренда",
    formInstagram: "Instagram (необязательно)",
    formCity: "Город",
    formCraft: "Вид ремесла",
    formExperience: "Опыт, лет",
    formProductCount: "Изделий готово к продаже",
    formMessage: "Сообщение (необязательно)",
    formContactSection: "Контактные данные",
    formWorkshopSection: "О мастерской",
    formConsent: "Согласен на использование данных командой Qolmura для обработки заявки.",
    formSubmit: "Отправить заявку",
    formSending: "Отправляем…",
    formSuccess: "Спасибо! Заявка принята, мы скоро свяжемся с вами.",
    formError: "Не удалось отправить. Попробуйте ещё раз или напишите в Instagram.",
    formOr: "Или свяжитесь напрямую",
    themeDark: "Тёмная тема",
  },
} as const

const values = [
  { icon: HeartHandshake, title: "stepOne", text: "stepOneText" },
  { icon: ShieldCheck, title: "stepTwo", text: "stepTwoText" },
  { icon: PackageCheck, title: "stepThree", text: "stepThreeText" },
] as const

function getInitialTheme(): Theme {
  const saved = localStorage.getItem("qolmura-theme")
  if (saved === "light" || saved === "dark") return saved
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
}

const emptySellerForm = {
  fullName: "",
  email: "",
  phone: "",
  brandName: "",
  instagram: "",
  city: "",
  craft: "",
  experienceYears: "",
  productCount: "",
  message: "",
  consent: false,
}

function App() {
  const [language, setLanguage] = useState<Language>("kk")
  const [theme, setTheme] = useState<Theme>(getInitialTheme)
  const [mobileMenu, setMobileMenu] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [audienceTab, setAudienceTab] = useState("buyer")
  const [featured, setFeatured] = useState<Product[]>([])
  const [featuredLoading, setFeaturedLoading] = useState(true)
  const [sellerForm, setSellerForm] = useState(emptySellerForm)
  const [sellerSheetOpen, setSellerSheetOpen] = useState(false)
  const [sellerStatus, setSellerStatus] = useState<"idle" | "sending" | "success" | "error">("idle")
  const [sellerError, setSellerError] = useState("")
  const searchRef = useRef<HTMLInputElement>(null)
  const t = content[language]
  const scrolled = useScrolled()
  const adminUrl = import.meta.env.VITE_ADMIN_URL ?? "/admin/"
  useReveal([language, featured])

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark")
    document.documentElement.style.colorScheme = theme
    localStorage.setItem("qolmura-theme", theme)
  }, [theme])

  useEffect(() => {
    if (window.location.pathname !== "/") { setFeaturedLoading(false); return }
    const controller = new AbortController()
    getProducts(new URLSearchParams(), controller.signal)
      .then((data) => setFeatured(data.results.slice(0, 4)))
      .catch((requestError: unknown) => {
        if (requestError instanceof DOMException && requestError.name === "AbortError") return
      })
      .finally(() => { if (!controller.signal.aborted) setFeaturedLoading(false) })
    return () => controller.abort()
  }, [])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener("keydown", onKeyDown)
    return () => window.removeEventListener("keydown", onKeyDown)
  }, [])

  function submitSearch(event: FormEvent) {
    event.preventDefault()
    const query = searchQuery.trim()
    window.location.href = `/catalog${query ? `?search=${encodeURIComponent(query)}` : ""}`
  }

  function submitSellerForm(event: FormEvent) {
    event.preventDefault()
    if (
      !sellerForm.fullName.trim() || !sellerForm.email.trim() || !sellerForm.phone.trim() ||
      sellerForm.phone.replace(/\D/g, "").length < 10 || !sellerForm.city.trim() ||
      !sellerForm.craft.trim() || !sellerForm.consent
    ) {
      setSellerStatus("error")
      setSellerError(t.formError)
      return
    }
    setSellerStatus("sending")
    submitSellerApplication({
      full_name: sellerForm.fullName.trim(),
      email: sellerForm.email.trim(),
      phone: sellerForm.phone.trim(),
      brand_name: sellerForm.brandName.trim(),
      instagram: sellerForm.instagram.trim(),
      city: sellerForm.city.trim(),
      craft: sellerForm.craft.trim(),
      experience_years: sellerForm.experienceYears ? Number(sellerForm.experienceYears) : undefined,
      estimated_product_count: sellerForm.productCount ? Number(sellerForm.productCount) : undefined,
      message: sellerForm.message.trim(),
      consent: sellerForm.consent,
    })
      .then(() => {
        setSellerStatus("success")
        setSellerForm(emptySellerForm)
      })
      .catch(() => {
        setSellerStatus("error")
        setSellerError(t.formError)
      })
  }

  if (window.location.pathname === "/catalog") {
    return <CatalogPage language={language} theme={theme} onLanguageChange={() => setLanguage(language === "kk" ? "ru" : "kk")} onThemeChange={() => setTheme(theme === "light" ? "dark" : "light")} />
  }

  if (window.location.pathname.startsWith("/products/")) {
    const slug = window.location.pathname.split("/").filter(Boolean)[1] ?? ""
    return <ProductDetailPage slug={slug} language={language} theme={theme} onLanguageChange={() => setLanguage(language === "kk" ? "ru" : "kk")} onThemeChange={() => setTheme(theme === "light" ? "dark" : "light")} />
  }

  return (
    <div className="app-shell">
      <header className="site-header" data-scrolled={scrolled}>
        <div className="container header-grid">
          <a href="#top" className="brand" aria-label="Qolmura">
            <img src="/qolmura-mark.png" alt="" />
            <span>QOLMURA</span>
          </a>

          <form className="search-form" onSubmit={submitSearch} role="search">
            <Search aria-hidden="true" />
            <Input ref={searchRef} value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} placeholder={t.search} aria-label={t.search} />
            <Button type="submit" variant="ghost" size="icon" className="search-submit" aria-label="Іздеу"><ArrowRight /></Button>
          </form>

          <div className="header-actions">
            <Button asChild variant="outline" size="sm" className="catalog-nav-btn"><a href="/catalog"><LayoutGrid />{t.catalog}</a></Button>
            <Button variant="ghost" size="sm" onClick={() => setLanguage(language === "kk" ? "ru" : "kk")} aria-label="Тілді ауыстыру">
              {language === "kk" ? "ҚАЗ" : "RU"}
            </Button>
            <Button variant="ghost" size="icon" onClick={() => setTheme(theme === "light" ? "dark" : "light")} aria-label={theme === "light" ? t.themeDark : t.themeLight}>
              <span key={theme} className="theme-icon">{theme === "light" ? <Moon /> : <Sun />}</span>
            </Button>
            <Button asChild variant="ghost" size="icon" className="hidden sm:inline-flex" aria-label={t.login}>
              <a href={adminUrl}><UserRound /></a>
            </Button>
            <Button className="desktop-seller" size="sm" onClick={() => setSellerSheetOpen(true)}><Store />{t.seller}</Button>
            <Sheet open={sellerSheetOpen} onOpenChange={(open) => {
              setSellerSheetOpen(open)
              if (!open && sellerStatus === "success") setSellerStatus("idle")
            }}>
              <SheetContent className="seller-sheet overflow-y-auto">
                <span className="seller-sheet-kicker">QOLMURA · SELLER ONBOARDING</span>
                <SheetTitle className="seller-sheet-title">{t.artisanCta}</SheetTitle>
                <SheetDescription className="seller-sheet-description">{t.artisanCtaText}</SheetDescription>

                {sellerStatus === "success" ? (
                  <div className="seller-success"><Check /><p>{t.formSuccess}</p></div>
                ) : (
                  <form className="seller-form" onSubmit={submitSellerForm}>
                    <div className="seller-form-section-title"><span>01</span><strong>{t.formContactSection}</strong></div>
                    <div className="seller-field">
                      <Label htmlFor="seller-name">{t.formName} *</Label>
                      <Input id="seller-name" name="fullName" autoComplete="name" required value={sellerForm.fullName} onChange={(event) => setSellerForm((form) => ({ ...form, fullName: event.target.value }))} />
                    </div>
                    <div className="seller-form-row">
                      <div className="seller-field">
                        <Label htmlFor="seller-email">{t.formEmail} *</Label>
                        <Input id="seller-email" name="email" type="email" autoComplete="email" required value={sellerForm.email} onChange={(event) => setSellerForm((form) => ({ ...form, email: event.target.value }))} />
                      </div>
                      <div className="seller-field">
                        <Label htmlFor="seller-phone">{t.formPhone} *</Label>
                        <Input id="seller-phone" name="phone" type="tel" autoComplete="tel" required placeholder="+7 700 000 00 00" value={sellerForm.phone} onChange={(event) => setSellerForm((form) => ({ ...form, phone: event.target.value }))} />
                      </div>
                    </div>
                    <Separator className="seller-form-separator" />
                    <div className="seller-form-section-title"><span>02</span><strong>{t.formWorkshopSection}</strong></div>
                    <div className="seller-form-row">
                      <div className="seller-field">
                        <Label htmlFor="seller-city">{t.formCity} *</Label>
                        <Input id="seller-city" name="city" autoComplete="address-level2" required value={sellerForm.city} onChange={(event) => setSellerForm((form) => ({ ...form, city: event.target.value }))} />
                      </div>
                      <div className="seller-field">
                        <Label htmlFor="seller-brand">{t.formBrand}</Label>
                        <Input id="seller-brand" name="brandName" value={sellerForm.brandName} onChange={(event) => setSellerForm((form) => ({ ...form, brandName: event.target.value }))} />
                      </div>
                    </div>
                    <div className="seller-field">
                      <Label htmlFor="seller-craft">{t.formCraft} *</Label>
                      <Input id="seller-craft" name="craft" required value={sellerForm.craft} onChange={(event) => setSellerForm((form) => ({ ...form, craft: event.target.value }))} />
                    </div>
                    <div className="seller-form-row">
                      <div className="seller-field">
                        <Label htmlFor="seller-experience">{t.formExperience}</Label>
                        <Input id="seller-experience" name="experienceYears" type="number" min="0" max="80" inputMode="numeric" value={sellerForm.experienceYears} onChange={(event) => setSellerForm((form) => ({ ...form, experienceYears: event.target.value }))} />
                      </div>
                      <div className="seller-field">
                        <Label htmlFor="seller-products">{t.formProductCount}</Label>
                        <Input id="seller-products" name="productCount" type="number" min="0" max="10000" inputMode="numeric" value={sellerForm.productCount} onChange={(event) => setSellerForm((form) => ({ ...form, productCount: event.target.value }))} />
                      </div>
                    </div>
                    <div className="seller-field">
                      <Label htmlFor="seller-instagram">{t.formInstagram}</Label>
                      <Input id="seller-instagram" name="instagram" placeholder="@username" value={sellerForm.instagram} onChange={(event) => setSellerForm((form) => ({ ...form, instagram: event.target.value }))} />
                    </div>
                    <div className="seller-field">
                      <Label htmlFor="seller-message">{t.formMessage}</Label>
                      <Textarea id="seller-message" name="message" value={sellerForm.message} onChange={(event) => setSellerForm((form) => ({ ...form, message: event.target.value }))} />
                    </div>
                    <div className="seller-consent">
                      <Checkbox id="seller-consent" checked={sellerForm.consent} onCheckedChange={(checked) => setSellerForm((form) => ({ ...form, consent: checked === true }))} />
                      <Label htmlFor="seller-consent">{t.formConsent}</Label>
                    </div>
                    {sellerStatus === "error" && <p className="seller-form-error">{sellerError}</p>}
                    <Button className="seller-submit" type="submit" size="lg" disabled={sellerStatus === "sending"}>{sellerStatus === "sending" ? t.formSending : t.formSubmit}<ArrowRight /></Button>
                  </form>
                )}

                <div className="application-panel">
                  <p>{t.formOr}</p>
                  <a href="https://www.instagram.com/qolmura.kz/" target="_blank" rel="noreferrer">Instagram · @qolmura.kz<ArrowRight /></a>
                  <a href="tel:+77075147960">{t.contact} · +7 707 514 79 60<ArrowRight /></a>
                </div>
              </SheetContent>
            </Sheet>
            <Button variant="ghost" size="icon" className="menu-trigger" onClick={() => setMobileMenu((open) => !open)} aria-label={mobileMenu ? t.close : t.menu}>
              {mobileMenu ? <X /> : <Menu />}
            </Button>
          </div>
        </div>

        <div className="desktop-nav-border">
          <nav className="container desktop-nav" aria-label="Негізгі навигация">
            <a href="#about">{t.about}</a>
            <a href="#artisans">{t.forArtisans}</a>
            <a href="#faq">{t.faq}</a>
          </nav>
        </div>

        {mobileMenu && (
            <nav className="mobile-nav mobile-nav-open" aria-label={t.menu}>
              <form className="mobile-search" onSubmit={submitSearch}><Search /><Input value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} placeholder={t.search} /><Button type="submit" variant="ghost" size="icon" aria-label="Іздеу"><ArrowRight /></Button></form>
              {[{ href: "#about", label: t.about }, { href: "/catalog", label: t.catalog }, { href: "#artisans", label: t.forArtisans }, { href: "#faq", label: t.faq }].map((item) => (
                <a key={item.href} href={item.href} onClick={() => setMobileMenu(false)}>{item.label}<ArrowRight /></a>
              ))}
              <Button className="mobile-seller-button" onClick={() => { setMobileMenu(false); setSellerSheetOpen(true) }}><Store />{t.seller}<ArrowRight /></Button>
            </nav>
        )}
      </header>

      <main id="top">
        <section className="hero-section">
          <div className="container hero-grid">
            <div className="hero-copy hero-reveal">
              <Badge className="hero-badge"><span className="badge-mark" />{t.eyebrow}</Badge>
              <h1>{t.title}</h1>
              <p>{t.lead}</p>
              <div className="hero-actions">
                <Button asChild size="lg"><a href="#about">{t.primary}<ArrowRight /></a></Button>
                <Button asChild size="lg" variant="outline"><a href="#artisans">{t.secondary}</a></Button>
              </div>
              <div className="hero-note">
                <span>01</span>
                <p>{t.officialText}</p>
              </div>
            </div>

            <div className="heritage-stage stage-reveal">
              <div className="heritage-top">
                <span>{t.official}</span>
                <a href="https://www.instagram.com/qolmura.kz/" target="_blank" rel="noreferrer"><Instagram />@qolmura.kz</a>
              </div>
              <div className="heritage-center">
                <div className="seal-frame"><img src="/qolmura-mark.png" alt="Qolmura" /></div>
                <span>QOLMURA</span>
              </div>
              <div className="heritage-copy">
                <OrnamentBand />
                <p>{t.officialBio}</p>
              </div>
            </div>
          </div>
        </section>

        {(featuredLoading || featured.length > 0) && (
          <section className="featured-section" id="featured">
            <div className="container">
              <div className="section-heading reveal">
                <div><span>02 / {t.featuredEyebrow}</span><h2>{t.featuredTitle}</h2></div>
                <div className="featured-heading-side">
                  <p>{t.featuredLead}</p>
                  <Button asChild variant="outline" size="sm"><a href="/catalog">{t.featuredCta}<ArrowRight /></a></Button>
                </div>
              </div>
              {featuredLoading ? (
                <div className="featured-loading"><div className="catalog-loader" /></div>
              ) : (
                <div className="product-grid reveal-stagger">
                  {featured.map((product) => (
                    <div className="reveal-item" key={product.id}>
                      <MarketplaceProductCard product={product} language={language} labels={{
                        one: t.uniqueBadge,
                        verified: t.verifiedBadge,
                        favorite: t.favorite,
                        removeFavorite: t.removeFavorite,
                        open: t.openProduct,
                        from: language === "kk" ? "бастап" : "от",
                      }} />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>
        )}

        <section className="stats-band reveal">
          <div className="container stats-grid">
            <div><Sparkles /><strong>100%</strong><span>{t.stat1}</span></div>
            <div><LayoutGrid /><strong>8</strong><span>{t.stat2}</span></div>
            <div><Truck /><strong>2–5</strong><span>{t.stat3}</span></div>
            <div><Gem /><strong>1/1</strong><span>{t.stat4}</span></div>
          </div>
        </section>

        <section className="about-section" id="about">
          <div className="container about-grid">
            <div className="section-intro reveal">
              <span className="section-index">03 / QOLMURA</span>
              <h2>{t.whyTitle}</h2>
              <p>{t.whyLead}</p>
            </div>
            <Tabs defaultValue="buyer" className="audience-tabs reveal" onValueChange={setAudienceTab}>
              <TabsList><TabsTrigger value="buyer">{t.buyerTab}</TabsTrigger><TabsTrigger value="artisan">{t.artisanTab}</TabsTrigger></TabsList>
              <TabsContent value="buyer"><AudiencePanel key={audienceTab} icon={PackageCheck} title={t.buyerTitle} text={t.buyerText} /></TabsContent>
              <TabsContent value="artisan"><AudiencePanel key={audienceTab} icon={Store} title={t.artisanTitle} text={t.artisanText} /></TabsContent>
            </Tabs>
          </div>
        </section>

        <section className="values-section" id="values">
          <div className="container">
            <div className="section-heading reveal"><div><span>04 / ҰСТАНЫМ</span><h2>{t.valuesTitle}</h2></div><p>{t.valuesLead}</p></div>
            <div className="value-grid reveal-stagger">
              {values.map(({ icon: Icon, title, text }, index) => (
                <article key={title} className="reveal-item">
                  <div className="value-head"><span className="value-number">0{index + 1}</span><Icon /></div><h3>{t[title]}</h3><p>{t[text]}</p><span className="value-line" />
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="statement-section">
          <div className="container statement-inner reveal">
            <div className="statement-mark"><img src="/qolmura-mark.png" alt="" /></div>
            <div><OrnamentBand /><blockquote>“{t.statement}”</blockquote><p>{t.statementSource}</p></div>
          </div>
        </section>

        <section className="artisan-section" id="artisans">
          <div className="container artisan-inner reveal">
            <div className="artisan-copy"><span>05 / ШЕБЕРЛЕРГЕ</span><h2>{t.artisanCta}</h2></div>
            <div className="artisan-action"><p>{t.artisanCtaText}</p><Button size="lg" onClick={() => setSellerSheetOpen(true)}>{t.apply}<ArrowRight /></Button></div>
            <div className="artisan-ornament" aria-hidden="true"><OrnamentBand /></div>
          </div>
        </section>

        <section className="faq-section" id="faq">
          <div className="container faq-grid reveal"><div><span>06 / FAQ</span><h2>{t.faqTitle}</h2></div><Accordion type="single" collapsible className="faq-accordion"><AccordionItem value="q1"><AccordionTrigger>{t.q1}</AccordionTrigger><AccordionContent>{t.a1}</AccordionContent></AccordionItem><AccordionItem value="q2"><AccordionTrigger>{t.q2}</AccordionTrigger><AccordionContent>{t.a2}</AccordionContent></AccordionItem><AccordionItem value="q3"><AccordionTrigger>{t.q3}</AccordionTrigger><AccordionContent>{t.a3}</AccordionContent></AccordionItem></Accordion></div>
        </section>
      </main>

      <footer>
        <div className="container footer-grid"><div><a href="#top" className="brand"><img src="/qolmura-mark.png" alt="" /><span>QOLMURA</span></a><p>{t.mission}</p></div><nav><a href="#about">{t.about}</a><a href="#artisans">{t.forArtisans}</a><a href="#faq">FAQ</a></nav><div className="footer-contact"><a href="https://www.instagram.com/qolmura.kz/" target="_blank" rel="noreferrer"><Instagram />@qolmura.kz</a><a href="tel:+77075147960">+7 707 514 79 60</a></div></div>
        <div className="container footer-bottom"><span>© 2026 Qolmura</span><span>Қазақстан</span></div>
      </footer>

    </div>
  )
}

function AudiencePanel({ icon: Icon, title, text }: { icon: typeof Check; title: string; text: string }) {
  return <div className="audience-panel" style={{ animation: "panel-in .5s cubic-bezier(.22,1,.36,1) both" }}><div className="audience-icon"><Icon /></div><h3>{title}</h3><p>{text}</p><ul><li><Check />Qolmura</li><li><Check />Қазақстан қолөнері</li></ul></div>
}

function OrnamentBand() {
  return <div className="ornament-band" aria-hidden="true">{Array.from({ length: 9 }, (_, index) => <span key={index}><i /></span>)}</div>
}

export default App
