from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "gender",
        "age",
        "country",
        "city",
    )


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
    )
