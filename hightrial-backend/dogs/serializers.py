from rest_framework import serializers
from .models import Dog

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ('id', 'name', 'owner', 'sire', 'dam', 'sex', 'color')
