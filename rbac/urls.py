"""djangoProject URL Configuration

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
from django.conf.urls import url
from rbac import views

urlpatterns = [

    url(r'^role/list/', views.role_list, name='role_list'),
    url(r'^role/add/', views.role_add, name='role_add'),
    url(r'^role/edit/(\d+)', views.role_edit, name='role_edit'),
    url(r'^role/del/(\d+)', views.role_del, name='role_del'),


    url(r'^menu/list/', views.menu_list, name='menu_list'),
    url(r'^menu/add/', views.menu_add, name='menu_add'),
    url(r'^menu/edit/(\d+)', views.menu_edit, name='menu_edit'),
    url(r'^menu/del/(\d+)', views.menu_del, name='menu_del'),

    url(r'^permission/add/', views.permission_add, name='permission_add'),
    url(r'^permission/edit/(\d+)', views.permission_edit, name='permission_edit'),
    url(r'^permission/del/(\d+)', views.permission_del, name='permission_del'),

    url(r'^distribute/permissions/', views.distribute_permissions, name='distribute_permissions')

]
