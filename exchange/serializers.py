from rest_framework import serializers
from exchange.models import rateData


class rateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = rateData
        fields = ['base_currency', 'target_currency', 'date', 'rate']



