from django.conf.urls import url,include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import logout
from django.views.generic import TemplateView


router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet, base_name='account-view')
router.register(r'products', views.ProductViewSet, base_name='product-list')
router.register(r'ratings', views.RatingViewSet, base_name='rating-list')
router.register(r'cart', views.CartViewSet,base_name='cart')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.MainPage.as_view()),
    url(r'^login/$', views.login_page, {'next_page': '/'}),
    url(r'^logout/$', logout, {'next_page': '/logged_out'}),
    url(r'^logged_out/$', TemplateView.as_view(template_name='logged_out.html')),

]
urlpatterns += [url(r'^api-token-auth/', obtain_auth_token), ]
