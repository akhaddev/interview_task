from rest_framework import serializers 
from .models import Menu



class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'name',
            'description',
            'price',
            'tags'
        )
    

class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'id',
            'guid',
            'name',
            'description',
            'price',
            'tags'
        )
