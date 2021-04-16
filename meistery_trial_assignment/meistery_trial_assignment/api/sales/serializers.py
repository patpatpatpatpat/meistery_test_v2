from sales.models import Sale

from rest_framework import serializers


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = (
            'id',
            'product',
            'revenue',
            'sales_number',
            'date',
            'user',  # TODO: rename to user_id
        )
