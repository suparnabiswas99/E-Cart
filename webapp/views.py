from .models import Product, Ratings, Cart
from .serializers import ProductSerializer, AccountSerializer, RatingSerializer, CartSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins, views
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import status


def avg_rating(p):
    total = 0
    count = 0
    for rating in Ratings.objects.all():
        if p.pk == rating.Product_Name.pk:
            count += 1
            total += rating.stars
    val = 4
    if count > 0:
        val = total/count
    return val


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    for product in Product.objects.all():
        product.avg_ratings = avg_rating(product)
        product.save()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RatingViewSet(viewsets.ModelViewSet):
    model = Ratings
    serializer_class = RatingSerializer
    def get_queryset(self):
        return Ratings.objects.filter(Cart.user = self.request.user)


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(AccountSerializer(request.user, context={'request': request}).data)
        return super(AccountViewSet, self).retrieve(request, pk)


class CartViewSet(viewsets.ModelViewSet):
    model = Cart
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def add(self, pk):
        '''
            create product and add it to the cart represented by pk
        '''
        product = Product.objects.get(pk=pk)
        cart = Cart.objects.get(user=self.request.user)
        cart.items.append(product)
        cart.save()
        return Response({"success": True})

    def pre_save(self, obj):
        obj.user = self.request.user

