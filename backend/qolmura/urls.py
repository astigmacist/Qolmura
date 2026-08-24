from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from marketplace.admin import qolmura_admin_site

urlpatterns = [
    path("admin/", qolmura_admin_site.urls),
    path("api/v1/", include("marketplace.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
