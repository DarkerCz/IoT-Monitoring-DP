# -*- coding: UTF-8 -*-

from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'monitoring'

urlpatterns = [
    # Prihlasovani, odhlasovani
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.IndexView.as_view(), name='index'),

    # Brany - Gateway
    path('gateway/list', views.GatewayListView.as_view(), name='gateway-list'),
    path('gateway/zpravy', views.GatewayZpravyListView.as_view(), name='gateway-zpravy'),
    path('gateway/create', views.GatewayCreateView.as_view(), name='gateway-create'),
    path('gateway/<int:pk>/edit/', views.GatewayEditView.as_view(), name='gateway-edit'),

    # Zarizeni
    path('zarizeni/list', views.ZarizeniListView.as_view(), name='zarizeni-list'),
    path('zarizeni/zpravy', views.ZarizeniZpravyListView.as_view(), name='zarizeni-zpravy'),
    path('zarizeni/create', views.ZarizeniCreateView.as_view(), name='zarizeni-create'),
    path('zarizeni/<int:pk>/edit/', views.ZarizeniEditView.as_view(), name='zarizeni-edit'),

    # Uzivatele
    path('uzivatel/list', views.UzivatelListView.as_view(), name='uzivatel-list'),
    path('uzivatel/create', views.UzivatelCreateView.as_view(), name='uzivatel-create'),
    path('uzivatel/<int:pk>/edit/', views.UzivatelEditView.as_view(), name='uzivatel-edit'),
]