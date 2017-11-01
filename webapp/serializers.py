from .models import Product, Ratings, Cart
from django.contrib.auth.models import User
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('Product_Name', 'price', 'rating')


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()
        return user


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'items', 'quantity')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ('cart', 'stars')

    # def validate(self, attrs):
    #     cart =  Cart.objects.get(user = attrs['user'], items=attrs['Product_Name'])
    #     if cart:
    #         return True
    #     else:
    #         return False
