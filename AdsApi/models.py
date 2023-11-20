from django.db import models

class AdsModel(models.Model):
    ad_name = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(auto_now=False)

    def __str__(self):
        return self.ad_name

class AdsLocationModel(models.Model):
    location_name = models.CharField(max_length=100)
    ad_id = models.ForeignKey(AdsModel, on_delete=models.CASCADE)

class RequestCount(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    ad = models.ForeignKey(AdsModel, on_delete=models.CASCADE) 