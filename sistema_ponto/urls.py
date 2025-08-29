"""
URL configuration for sistema_ponto project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Django admin renomeado
    path('', include('ponto.urls')),  # URLs da nossa app
]

# Servir arquivos de media durante desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Configurações do Django Admin
admin.site.site_header = "Sistema de Ponto - Administração"
admin.site.site_title = "Sistema de Ponto"
admin.site.index_title = "Painel Administrativo"