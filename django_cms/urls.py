"""
URL configuration for django_cms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from user.views.login_view import CustomTokenView

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"authenticate/token/$", CustomTokenView.as_view(), name="token"),

    re_path('user/', include('user.urls')),
    re_path('content/', include('content.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

admin.site.site_header = 'Architech\'s Content Management Server'

