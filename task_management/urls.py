from django.conf.urls import url
from django.contrib import admin

from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', views.Login.as_view(), name='loginview')
]
