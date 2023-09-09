from rest_framework import serializers
from .models import Event

#Serializer for Events
class EventSerializer(serializers.ModelSerializer):

    # img_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Event
        fields = '__all__'
    # def get_image_url(self, obj):
    #     request = self.context
    #     return request
        # return request.build_absolute_uri(obj.img.url)

