# Qolmura marketplace

Minimalist national marketplace for Kazakhstan's artisans. The project combines a React 19 storefront with a Django 5.2 API and an operations admin panel.

## Structure

- `frontend/` — React 19, TypeScript, Vite, Tailwind CSS 4 and shadcn/ui components.
- `backend/` — Django 5.2 LTS, Django REST Framework, catalog, seller applications and branded staff admin.
- `docs/PRODUCT-AND-SYSTEM-DESIGN.md` — product analysis, architecture, scale path, and delivery plan.
- original brand and research materials remain in the workspace root.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The development server proxies `/api`, `/admin` and `/static` to Django on `127.0.0.1:8000`. The storefront is available at `http://127.0.0.1:5173`, and the admin opens through `http://127.0.0.1:5173/admin/`.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
QOLMURA_ADMIN_PASSWORD='choose-a-local-password' python manage.py ensure_admin
python manage.py seed_demo
python manage.py runserver
```

SQLite is used only for local development. Seller submissions are sent to `POST /api/v1/seller-applications/` and are processed by staff at `http://127.0.0.1:8000/admin/`.

## Admin workflow

The Django admin is the secure operations panel. Staff can:

- create and edit categories, artisans and bilingual product cards;
- publish, archive and feature products;
- receive seller applications with name, email, phone, city, workshop, craft, experience and available inventory;
- assign an application to a manager, add internal notes and move it through `new → in review → contacted → approved/rejected`;
- use bulk actions for application processing.

Never commit an admin password. `ensure_admin` reads `QOLMURA_ADMIN_USERNAME`, `QOLMURA_ADMIN_EMAIL` and `QOLMURA_ADMIN_PASSWORD` from the environment.

## Deploying to Vercel

This monorepo is deployed as two Vercel projects from the same GitHub repository. This keeps the Vite SPA and Django runtime independently configurable.

### 1. Database

Create a managed PostgreSQL database from the Vercel Marketplace (Neon or another supported provider). A persistent external database is required: Vercel Functions do not provide persistent SQLite storage.

### 2. Backend project

Create a Vercel project with **Root Directory** set to `backend`. Configure:

```env
DJANGO_SECRET_KEY=long-random-secret
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=.vercel.app
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
QOLMURA_PUBLIC_SITE_URL=https://your-frontend.vercel.app
QOLMURA_ADMIN_USERNAME=admin
QOLMURA_ADMIN_EMAIL=admin@example.com
QOLMURA_ADMIN_PASSWORD=strong-unique-password
```

The backend build runs migrations, collects admin assets, loads the idempotent demo collection and creates the administrator when its password is configured. Django is then available at `/api/v1/` and `/admin/`.

### 3. Frontend project

Create a second Vercel project with **Root Directory** set to `frontend`.

`frontend/vercel.json` redirects `/admin`, `/api` and Django static paths to the deployed backend before applying the SPA fallback. The public admin entry point is `https://qolmura.vercel.app/admin/`; Vercel then sends staff to the secure Django deployment. Direct visits to `/catalog` and `/products/:slug` still return `index.html` and are handled by React. The production frontend also uses `VITE_API_BASE_URL` and `VITE_ADMIN_URL` to access Django directly.

The storefront requests Django first and has a bundled copy of the six demo products as a read-only availability fallback. Product and seller-application changes still come from Django; the fallback only prevents an empty catalog while the API is unavailable.

For production editing, configure `DATABASE_URL` on the backend project with a managed PostgreSQL database. SQLite bundled inside a Vercel Function is suitable only for the seeded read-only demo and must not be used as persistent production storage.

Vercel does not need to be added to the application dependencies. Run the current CLI on demand for local checks:

```bash
cd frontend
npx vercel@latest --version
npm run build
```
