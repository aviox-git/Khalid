from rest_framework import serializers
from . models import PromotionModel
class PromotionSerialiser(serializers.ModelSerializer):

    class Meta:
        model = PromotionModel
        fields = '__all__'
