from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView # Yönlendirme için gerekli
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# --- Swagger Yapılandırması ---
schema_view = get_schema_view(
   openapi.Info(
      title="Stock_App API",
      default_version='v1',
      description="Stock_App API Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="umitarat8098@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# --- Ana URL Listesi ---
urlpatterns = [
    # 1. Kök dizine (https://umit8103.pythonanywhere.com/) geleni swagger'a yönlendir
    path('', RedirectView.as_view(url='swagger/', permanent=True)),
    
    # 2. Mevcut Uygulama Yolları
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')),
    path('stock/', include('stock.urls')),

    # 3. Swagger & Redoc Yolları
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# --- Debug Toolbar (Sadece Geliştirme Ortamında Çalışır) ---
if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

# --- Statik ve Medya Dosyaları ---
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)