"""Donation_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
import backendapp.urls
import frontendapp.urls

from django.contrib.staticfiles.urls import staticfiles_urlpatterns,static
from Donation_Project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('donation/', include(backendapp.urls)),
    path('', include(frontendapp.urls)),

]


urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)