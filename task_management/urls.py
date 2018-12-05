from django.conf.urls import url
from django.contrib import admin

from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^notifications$', views.getNotifications),
    url(r'^update/notification$', views.updateNotification),
    url(r'^task/all$', views.getTasksList),
    url(r'^task/new$', views.getNewTasksList),
    url(r'^task/create/$', views.createTask, name='createNewTask'),
    url(r'^task/update/$', views.updateTask, name='updateTask'),
    url(r'^logout/$', views.Logout.as_view(), name='logoutview'),
    url(r'^login/$', views.Login.as_view(), name='loginview'),
    url(r'^', views.Dashboard.as_view()),
]
