from django.contrib import admin
from django.urls import path, include
from .views import AdsCUD, AdsViews, LocationViews, RecounterView
from rest_framework import routers

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('Ads/', AdsViews.as_view(), name='ads_list'),
    path('Ads/<int:pk>/', AdsViews.as_view(), name='ads_detail'),
    path('create_ads/', AdsCUD.as_view(), name='create_ads'),
    path('update_ads/<int:pk>/', AdsCUD.as_view(), name='update_ads'),
    path('delete_ads/<int:pk>/', AdsCUD.as_view(), name='delete_ads'),
    path('location/', LocationViews.as_view(), name='location_list'),
    path('location/<int:pk>/', LocationViews.as_view(), name='location_detail'),
    path('create_location/', AdsCUD.as_view(), name='create_location'),
    path('update_location/<int:pk>/', AdsCUD.as_view(), name='update_location'),
    path('delete_location/<int:pk>/', AdsCUD.as_view(), name='delete_location'),
    path('request_count/', RecounterView.as_view(), name='request_count'),
    path('create_counter/', RecounterView.as_view(), name='create_counter'),
]
