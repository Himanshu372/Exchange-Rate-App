from django.db import models

# Create your models here.

from django.db import models
import datetime


class rateData(models.Model):
    base_currency = models.TextField(max_length = 3, null = False)
    target_currency = models.TextField(max_length = 3, null = False)
    date = models.CharField(max_length = 10, null=False)
    # from_date = models.CharField(max_length = 10, null=False)
    rate = models.FloatField(null = False)
    def __str__(self):
        return '{} to {} conversion rate is {}'.format(self.base_currency, self.target_currency, self.rate)

    # def save(self):
    #     if not self.from_time:
    #         date = datetime.datetime.strptime(self.to_date, '%Y-%m-%d').date()
    #         self.from_date = datetime.datetime.strftime(datetime.date(date.year, date.month - 2, date.day), '%Y-%m-%d')
    #     super(rateData, self).save()





