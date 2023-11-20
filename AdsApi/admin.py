from django.contrib import admin
from .models import AdsModel, AdsLocationModel, RequestCount

@admin.register(AdsModel)
class AdsModelAdmin(admin.ModelAdmin):
    list_display = ['ad_name', 'start_date', 'end_date']

@admin.register(AdsLocationModel)
class AdsLocationModelAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'ad_id']

@admin.register(RequestCount)
class RequestCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'ad']
