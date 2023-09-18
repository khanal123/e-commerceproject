from .models import *
from rest_framework import serializers 

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        # sabai fields lai rakhna parxa bhanne xaina but required fields lai rakhnai parne hunxa jun app ma chinxa nai 
        fields = ['id','title','price','discounted_price','image','slug','stock','brand','labels','special_offer','category','subcategory']


class AdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ad 
        fields = ['title','image','category']      

      