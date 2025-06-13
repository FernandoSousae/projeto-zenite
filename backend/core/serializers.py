# core/serializers.py
from rest_framework import serializers
from .models import PlanoCompra

class PlanoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoCompra
        fields = '__all__' # Por enquanto, vamos expor todos os campos do modelo