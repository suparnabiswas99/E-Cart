from django.contrib import admin
from .models import Product


class webAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ['Product_Name', 'price']

    class Meta:
        model = Product

admin.site.register(Product, webAdmin)
