from sales.models import Sale

from rest_framework import serializers


class SaleSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField("get_user_id")

    class Meta:
        model = Sale
        fields = (
            "id",
            "product",
            "revenue",
            "sales_number",
            "date",
            "user_id",
        )

    def get_user_id(self, obj):
        return obj.user.id
