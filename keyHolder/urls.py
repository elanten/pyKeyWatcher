"""keyHolder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from .views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^keys/', include('digital_key.urls')),
    url(r'^employees/', include('employee.urls')),
    url(r'^centers/', include('cert_center.urls')),
    url(r'^manuals/', include('key_manual.urls')),
    url(r'^export/', include('export.urls')),
]
