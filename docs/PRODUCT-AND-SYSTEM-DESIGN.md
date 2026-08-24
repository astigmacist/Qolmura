# Qolmura: product and system design v0.1

## 1. What we learned

Qolmura is a curated marketplace for Kazakh artisans, not a general classifieds site. Its strongest promise is: authentic work, a visible maker, a trustworthy purchase, and a modern way to preserve national craft.

Primary users:

- artisans from cities and villages who currently sell through Instagram, fairs, or direct messages;
- buyers looking for authentic national-style objects and distinctive gifts;
- international buyers interested in original Kazakh craft (later phase);
- corporate buyers looking for meaningful gifts and small wholesale runs (later phase).

The initial materials consistently identify four gaps: discovery, trust/authenticity, integrated payment and delivery, and promotion for artisans. The go-to-market hypothesis is free onboarding, zero commission for the first three months, visual/content support for makers, and a first-order delivery incentive for buyers.

## 2. Product positioning

**Qolmura is the trusted digital home of Kazakhstan's handmade culture.**

The experience should feel editorial and premium, but remain approachable to a new seller. National identity is expressed through proportion, texture, ornament rhythm, warm natural color, bilingual language, and maker stories—not through decorative overload.

Core experience principles:

1. The maker is as important as the product.
2. Authenticity and fulfilment are visible before checkout.
3. Search and categories solve the discovery problem Instagram cannot.
4. Kazakh is first-class; Russian is equally usable. English is a later expansion.
5. A one-of-a-kind item must never be oversold.

## 3. MVP use cases

Buyer:

- browse, search, filter, and sort products;
- open a product and see its maker, materials, dimensions, availability, delivery estimate, and authenticity status;
- save favourites, add to cart, checkout, and track an order;
- review a completed order and contact support.

Artisan:

- apply, verify identity, and create a shop profile;
- publish bilingual product listings with images, variants, stock, and lead time;
- accept and fulfil orders;
- see simple sales, views, conversion, and payout information.

Operations:

- moderate sellers and listings;
- resolve orders, refunds, complaints, and authenticity reports;
- curate featured collections and editorial stories;
- configure commissions and promotions.

## 4. High-level design

The system-design-primer recommends starting with use cases and constraints, then a high-level design, core components, and only then scale. Qolmura follows that sequence and starts as a **modular Django monolith**. This avoids premature microservices while preserving domain boundaries.

```text
React + Tailwind + shadcn UI
           |
      REST API / CDN
           |
 Django + Django REST Framework
  | catalog | sellers | orders |
  | payments | delivery | content |
           |
 PostgreSQL + object storage
           |
 Redis cache + Celery workers (when needed)
```

Initial deployment:

- React static assets behind a CDN;
- Django API behind a reverse proxy;
- PostgreSQL as the source of truth;
- S3-compatible object storage for product media;
- managed email/SMS, payment, and delivery providers through adapters;
- error tracking, structured logs, health checks, backups, and basic product analytics.

## 5. Domain boundaries

- **Identity**: buyers, artisans, staff, roles, verification.
- **Catalog**: categories, products, media, materials, variants, availability.
- **Discovery**: search, filters, collections, recommendations.
- **Commerce**: carts, orders, order items, prices, coupons, commissions.
- **Payment**: intents, provider callbacks, refunds, payouts, reconciliation.
- **Fulfilment**: addresses, delivery quotes, shipments, tracking events.
- **Trust**: moderation, authenticity review, ratings, disputes.
- **Content**: artisan stories, editorial collections, localized content.

These are Django apps/modules first. A module becomes a service only after operational evidence shows an independent scaling or ownership need.

## 6. Data and consistency

PostgreSQL is the right default because orders, inventory, payments, and payouts need relational constraints and ACID transactions.

Critical invariants:

- an active product references a verified artisan and an active category;
- order price is snapshotted in the order item and never recomputed from the current catalog;
- inventory reservation and order creation happen transactionally;
- payment and delivery webhooks are idempotent and stored with provider event IDs;
- a one-of-a-kind item has at most one active reservation;
- money uses decimal minor-unit-safe values and explicit currency.

## 7. API outline

Public:

- `GET /api/v1/categories/`
- `GET /api/v1/products/?search=&category__slug=&ordering=`
- `GET /api/v1/products/{slug}/`
- `GET /api/v1/artisans/{slug}/`

Authenticated additions:

- `POST /api/v1/cart/items/`
- `POST /api/v1/orders/`
- `POST /api/v1/payments/intents/`
- `GET /api/v1/orders/{id}/`
- seller CRUD under `/api/v1/seller/`

Mutation endpoints accept an `Idempotency-Key` where a retry could duplicate money, inventory, or fulfilment work.

## 8. Scale path

The primer's load balancing, caching, database, CDN, and asynchronous-processing patterns are introduced only as demand appears:

1. Cache static media through a CDN from day one.
2. Add Redis cache-aside for category trees, featured collections, and popular product reads; invalidate on admin updates.
3. Move image processing, notifications, search indexing, and reconciliation to Celery task queues.
4. Add PostgreSQL read replicas for catalog reads if DB read load becomes dominant.
5. Start search with PostgreSQL full-text/trigram indexes; introduce OpenSearch only when relevance, facets, or catalog size justify it.
6. Horizontally scale stateless Django instances behind a load balancer.
7. Partition analytics/event data before considering transactional database sharding.

## 9. Security and trust baseline

- secure cookies or short-lived tokens with rotation;
- CSRF protection for cookie-authenticated mutations;
- throttling on login, checkout, reviews, and uploads;
- MIME/type/size validation and malware scanning for uploads;
- signed private URLs for verification documents;
- least-privilege staff roles and audit logs for moderation/refunds;
- secrets only in environment/secret management;
- payment card data never touches Qolmura servers;
- daily encrypted backups plus tested restore procedures.

## 10. Delivery plan

Phase 1 — discovery vertical slice (complete): branded home, categories, search, favourites/cart interactions, catalog models, product detail and read API.

Phase 2 — real catalog (in progress): seller application onboarding, PostgreSQL-ready configuration, branded admin moderation and seed content are complete. Seller authentication, managed media upload and artisan self-service remain.

Phase 3 — commerce: cart persistence, checkout, payment adapter, inventory reservation, delivery quotes, order lifecycle, notifications.

Phase 4 — growth: reviews, stories, promotions, seller analytics, corporate orders, Kazakh/Russian CMS content, SEO.

## 11. Success metrics

- verified artisans activated (first product published);
- product-detail-to-add-to-cart conversion;
- checkout completion rate;
- repeat purchase rate at 30/90 days;
- fulfilled orders without support intervention;
- median time from artisan registration to first product;
- search zero-result rate;
- percentage of listings with complete bilingual content and strong imagery.
