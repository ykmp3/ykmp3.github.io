#!/usr/bin/env python
# coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^termsofuse', views.termsofuse, name='termsofuse'),
    url(r'^convert', views.convert, name='convert'),
    url(r'^news', views.news, name='news'),
    url(r'^contact', views.contact, name='contact'),
]
