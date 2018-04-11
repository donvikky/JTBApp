"""jtbapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url,include
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework import routers
from api import views

# api URLs
router = routers.DefaultRouter()
router.register(r'individual', views.IndividualTaxPayerViewset)
router.register(r'corporate', views.CorporateTaxPayerViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='index'),
    path('api/', include(router.urls)),
    path('apis/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
