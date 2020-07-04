"""py_project URL Configuration

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
from django.urls import path
from django.conf.urls import url

from py_start.views import project_index, pos_system_index, inner_login_page, manager_index, forecast

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', project_index),
    url(r'^pos_system_index/$', pos_system_index),
    url(r'^manager_index/$', manager_index),
    url(r'^inner_login_page/$', inner_login_page),
    url(r'^forecast/$', forecast),

]
