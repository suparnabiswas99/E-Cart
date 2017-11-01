from django.db import models
from .choices import RATING_CHOICES


# class RatingManager(models.Manager):
#     def avg_rating(self):
#         sum, count = 0, 0
#         for rating in Ratings:
#             if self.Product_Name == rating.Product_Name:
#                 count += 1
#                 sum += rating.stars
#         val = sum/count
#         return val
#

class Product(models.Model):
    Product_Name = models.CharField(max_length=120, null=True)
    price = models.IntegerField(default=0, null=False)

    def _get_rating(self):
        total = 0
        count = 0
        for rating in Ratings.objects.all():
            if self.pk == rating.cart.items.pk:
                count += 1
                total += rating.stars
        val = 4
        if count > 0:
            val = total / count
        return val
    rating = property(_get_rating)

    def __str__(self):
        return self.Product_Name


class Cart(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('auth.User', related_name="carts")
    items = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('items', 'user')

    def __str__(self):
        return self.user.username + "_" + self.items.Product_Name


class Ratings(models.Model):
    cart = models.OneToOneField(Cart)
    stars = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return self.cart + "-" + self.stars
