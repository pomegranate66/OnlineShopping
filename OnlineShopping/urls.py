"""OnlineShopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls.conf import re_path
from django.views.static import serve

from OnlineShopping.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    re_path(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    path('search/', include('haystack.urls')),  # 全文搜索框架
    path('', include('goods.urls')),
]
