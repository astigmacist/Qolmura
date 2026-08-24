import { useState } from "react"
import { ArrowUpRight, Heart, MapPin, ShieldCheck } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { resolveMediaUrl, type Product } from "@/lib/api"

type Language = "kk" | "ru"

type ProductCardLabels = {
  demo: string
  one: string
  verified: string
  favorite: string
  removeFavorite: string
  open: string
}

function readFavorites() {
  try {
    return new Set(JSON.parse(localStorage.getItem("qolmura-favorites") ?? "[]") as string[])
  } catch {
    return new Set<string>()
  }
}

export function MarketplaceProductCard({ product, language, labels }: {
  product: Product
  language: Language
  labels: ProductCardLabels
}) {
  const [favorite, setFavorite] = useState(() => readFavorites().has(product.slug))
  const name = language === "kk" ? product.name_kk : product.name_ru
  const category = language === "kk" ? product.category.name_kk : product.category.name_ru

  function toggleFavorite() {
    const values = readFavorites()
    if (values.has(product.slug)) values.delete(product.slug)
    else values.add(product.slug)
    localStorage.setItem("qolmura-favorites", JSON.stringify([...values]))
    setFavorite(values.has(product.slug))
  }

  return (
    <Card className="product-card">
      <div className="product-card-media">
        <a href={`/products/${product.slug}`} className="product-image" aria-label={name}>
          {product.cover_url ? (
            <img src={resolveMediaUrl(product.cover_url)} alt={name} loading="lazy" />
          ) : (
            <div className="product-placeholder"><img src="/qolmura-mark.png" alt="" /></div>
          )}
          <span className="product-open"><ArrowUpRight />{labels.open}</span>
        </a>
        <div className="product-badges">
          {product.is_demo && <Badge className="demo-badge">{labels.demo}</Badge>}
          {product.is_one_of_a_kind && <Badge>{labels.one}</Badge>}
        </div>
        <Button
          type="button"
          variant="secondary"
          size="icon"
          className="product-favorite"
          aria-label={favorite ? labels.removeFavorite : labels.favorite}
          aria-pressed={favorite}
          onClick={toggleFavorite}
        >
          <Heart fill={favorite ? "currentColor" : "none"} />
        </Button>
      </div>
      <CardContent className="product-info">
        <p>{category}</p>
        <h2><a href={`/products/${product.slug}`}>{name}</a></h2>
        <span className="artisan-meta"><MapPin />{product.artisan.shop_name} · {product.artisan.city}</span>
        <div>
          <strong>{new Intl.NumberFormat(language === "kk" ? "kk-KZ" : "ru-KZ").format(Number(product.price))} ₸</strong>
          <span><ShieldCheck />{labels.verified}</span>
        </div>
      </CardContent>
    </Card>
  )
}
