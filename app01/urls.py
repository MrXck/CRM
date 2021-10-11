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
from django.contrib import admin
from app01 import views

urlpatterns = [
    # 主页
    url(r'^home/', views.home, name='home'),

    # 客户信息有关
    url(r'^customers/', views.customers, name='customers'),
    url(r'^my_customers/', views.customers, name='my_customers'),
    url(r'^add_customer/', views.add_customer, name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.edit_customer, name='edit_customer'),
    # url(r'^delete_customer/(\d+)', views.delete_customer, name='delete_customer'),

    # 跟进记录有关
    url(r'^consult_record/', views.consult_record, name='consult_record'),
    url(r'^add_consult_record/', views.add_consult_record, name='add_consult_record'),
    url(r'^edit_consult_record/(\d+)/', views.edit_consult_record, name='edit_consult_record'),
    url(r'^delete_consult_record/(\d+)/', views.delete_consult_record, name='delete_consult_record'),

    # 报名信息有关
    url(r'^enrollment/', views.enrollment, name='enrollment'),
    url(r'^add_enrollment/', views.add_enrollment, name='add_enrollment'),
    url(r'^edit_enrollment/(\d+)/', views.edit_enrollment, name='edit_enrollment'),
    url(r'^delete_enrollment/(\d+)/', views.delete_enrollment, name='delete_enrollment'),

    # 课程记录有关
    url(r'^course_record/', views.course_record, name='course_record'),
    url(r'^add_course_record/', views.add_course_record, name='add_course_record'),
    url(r'^edit_course_record/(\d+)/', views.edit_course_record, name='edit_course_record'),

    # 学习记录有关
    url(r'^study_record/(\d+)/', views.study_record, name='study_record'),
    url(r'^add_study_record/', views.add_study_record, name='add_study_record'),
    url(r'^edit_study_record/(\d+)/', views.edit_study_record, name='edit_study_record'),
]
