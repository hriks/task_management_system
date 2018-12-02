from django.conf.urls import url
from django.contrib import admin

from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home', views.Dashboard.as_view()),
    url(r'^task/all', views.getTasksList),
    url(r'^task/new', views.getNewTasksList),
    url(r'^task/create', views.createTask, name='createNewTask'),
    url(r'^logout', views.Logout.as_view()),
    url(r'^', views.Login.as_view(), name='loginview')
]
