from rest_framework import serializers
from .models import Sponsor

#Serializer for Sponsors
class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = '__all__'
    
