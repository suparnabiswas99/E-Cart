from .models import Product, Ratings, Cart
from .serializers import ProductSerializer, AccountSerializer, RatingSerializer, CartSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from .forms import LoginForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login




class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RatingViewSet(viewsets.ModelViewSet):
    model = Ratings
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Ratings.objects.filter(cart__user=self.request.user)


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


class MainPage(LoginRequiredMixin, TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def login_page(request, next_page):
	context = {"declined": False}
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(request, username=form.cleaned_data['user_name'], password=form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(form.cleaned_data['next_page'])
			else:
				context['declined'] = True
	else:
		form = LoginForm()
		form.next_page = next_page

	context['form'] = form
	return render(request, 'login.html', context)

