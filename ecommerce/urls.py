"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_home(request):
    """Page d'accueil de l'API"""
    return JsonResponse({
        'message': 'Bienvenue sur l\'API de la Boutique E-commerce',
        'endpoints': {
            'products': '/api/products/',
            'orders': '/api/orders/',
            'admin': '/admin/',
        }
    })

def health_check(request):
    return JsonResponse({"status": "healthy", "message": "Ecommerce API is running"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/', include('products.urls')),  # Inclure les URLs des produits sous /api/
    path('api/', include('orders.urls')),    # Inclure les URLs des commandes sous /api/
    path('', api_home, name='api_home'),  # Page d'accueil de l'API à la racine
]

# Ajouter les URLs pour les fichiers média en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
