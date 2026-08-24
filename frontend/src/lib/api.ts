export type Category = {
  id: number
  name_kk: string
  name_ru: string
  slug: string
  image: string | null
  product_count: number
}

export type Artisan = {
  id: number
  shop_name: string
  slug: string
  city: string
  story_kk: string
  story_ru: string
  rating: string
  is_verified: boolean
}

export type Product = {
  id: number
  name_kk: string
  name_ru: string
  slug: string
  description_kk: string
  description_ru: string
  materials_kk: string
  materials_ru: string
  dimensions_kk: string
  dimensions_ru: string
  care_kk: string
  care_ru: string
  production_time_days: number
  cover_url: string
  price: string
  stock: number
  is_featured: boolean
  is_one_of_a_kind: boolean
  is_demo: boolean
  artisan: Artisan
  category: Category
}

export type PaginatedProducts = {
  count: number
  next: string | null
  previous: string | null
  results: Product[]
}

const apiBase = (import.meta.env.VITE_API_BASE_URL ?? "/api/v1").replace(/\/$/, "")

export function resolveMediaUrl(url: string) {
  if (!url) return ""
  try {
    const parsed = new URL(url)
    if (parsed.hostname === "127.0.0.1" && parsed.port === "5173") {
      return `${window.location.origin}${parsed.pathname}`
    }
  } catch {
    return url
  }
  return url
}

async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(path, { headers: { Accept: "application/json" }, signal })
  if (!response.ok) throw new Error(`API request failed with ${response.status}`)
  return response.json() as Promise<T>
}

export function getCategories(signal?: AbortSignal) {
  return request<{ results?: Category[] } | Category[]>(`${apiBase}/categories/`, signal).then((data) => Array.isArray(data) ? data : data.results ?? [])
}

export function getProducts(params: URLSearchParams, signal?: AbortSignal) {
  const query = params.toString()
  return request<PaginatedProducts>(`${apiBase}/products/${query ? `?${query}` : ""}`, signal)
}

export function getProduct(slug: string, signal?: AbortSignal) {
  return request<Product>(`${apiBase}/products/${encodeURIComponent(slug)}/`, signal)
}

export type SellerApplicationPayload = {
  full_name: string
  email: string
  phone: string
  brand_name?: string
  instagram?: string
  city: string
  craft: string
  experience_years?: number
  estimated_product_count?: number
  message?: string
  consent: boolean
}

export async function submitSellerApplication(payload: SellerApplicationPayload, signal?: AbortSignal) {
  const response = await fetch(`${apiBase}/seller-applications/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
    signal,
  })
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const message = data && typeof data === "object"
      ? Object.values(data as Record<string, unknown>).flat().join(" ")
      : `Request failed with ${response.status}`
    throw new Error(message || `Request failed with ${response.status}`)
  }
  return data
}
