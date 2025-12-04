from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
