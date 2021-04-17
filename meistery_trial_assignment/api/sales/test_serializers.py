import pytest

from .factories import SaleFactory
from django.utils import timezone
from . import serializers


class TestSaleSerializer:
    pytestmark = pytest.mark.django_db

    def test_serializer_model(self):
        today = timezone.now().date()
        sale = SaleFactory(date=today)

        serializer = serializers.SaleSerializer(sale)

        expected_data = {
            'id': sale.id,
            'product': sale.product,
            'revenue': sale.revenue,
            'sales_number': sale.sales_number,
            'user_id': sale.user.id,
            'date': sale.date.isoformat(),
        }

        assert serializer.data == expected_data
