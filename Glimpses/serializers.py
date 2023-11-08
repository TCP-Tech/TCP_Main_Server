from rest_framework import serializers
from .models import Glimpse

#Serializer for Glimpses
class GlimpseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Glimpse
        fields = '__all__'
    

