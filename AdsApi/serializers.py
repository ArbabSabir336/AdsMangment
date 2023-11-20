from rest_framework import serializers
from .models import AdsModel, AdsLocationModel, RequestCount

class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsModel
        fields = '__all__'

class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdsLocationModel
        fields = ('id', 'location_name', 'ad_id')

class RequestCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestCount
