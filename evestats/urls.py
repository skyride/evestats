"""evestats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from core import views as core_views
from search import views as search_views

urlpatterns = [
    path("", core_views.MarketGroupView.as_view(), name="index"),
    path("group/<int:marketgroup_id>", core_views.MarketGroupView.as_view(), name="market_group_view"),
    path("type/<int:type_id>", core_views.TypeView.as_view(), name="type_view"),
    path("dumps/types.json", search_views.TypeDump.as_view(), name="type_dump"),
    path("search/<str:search>", search_views.TypeSearch.as_view(), name="type_search"),
]