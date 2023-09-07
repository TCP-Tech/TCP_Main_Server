from rest_framework import serializers
from .models import Event

#Serializer for Events
class EventSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Event
        fields = ['year','title','date','img','description','instaLink','img_url']
    def get_image_url(self, obj):
        return obj.img.url
