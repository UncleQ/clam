"""stock_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
#from django.conf.urls import patterns, url
#from image import views
from . import stock_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', stock_views.home),
    path('test/', stock_views.test),
    path('mission/', stock_views.mission),
    path('submit/', stock_views.submit),
    path('stop_cur_mission/', stock_views.stop_cur_mission),
    path('show_last_image/', stock_views.show_last_image),
    path('add_data/', stock_views.add_data),
    path('add_label_line/', stock_views.add_label_line),
    #re_path(r'^image/pic_8p/(?P<path>.*)', 'django.views.static.serve', {'document_root':'/opt/work/stock/pic_8p'}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
