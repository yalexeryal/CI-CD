from rest_framework import serializers
from rest_framework.utils import model_meta

from logistic.models import StockProduct, Product, Stock


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for p in positions:
            StockProduct.objects.create(stock=stock, **p)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        positions_instance = instance.positions.all()
        w = 0
        for r in positions_instance:
            r.price = positions[w]['price']
            r.quantity = positions[w]['quantity']
            r.save()
            w += 1

        return stock