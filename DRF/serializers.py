from rest_framework import serializers
from .models import Country


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name', 'spoken_language', 'population']
