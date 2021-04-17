from django.db import models


class Sale(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    date = models.DateField()
    product = models.CharField(max_length=200)
    sales_number = models.PositiveIntegerField()
    revenue = models.FloatField()
