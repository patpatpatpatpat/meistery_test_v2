from django.contrib import admin

from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'product',
        'sales_number',
        'revenue',
    )
