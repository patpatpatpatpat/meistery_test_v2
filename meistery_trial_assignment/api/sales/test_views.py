import json
import pytest
from rest_framework import status

from meistery_trial_assignment.api.users.factories import UserFactory
from .factories import SaleFactory
from sales.models import Sale
from users.models import User
from django.utils import timezone

pytestmark = pytest.mark.django_db


class TestSalesAPI:
    endpoint = "/api/v1/sales/"

    def test_list_sales_for_current_user(self, api_client):
        user = UserFactory(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@test.com",
            gender=User.MALE,
            age=30,
        )
        sale = SaleFactory(user=user, date=timezone.now().date())
        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(self.endpoint)
        response_data = json.loads(response.content)
        expected_response = [
            {
                "id": sale.id,
                "product": sale.product,
                "revenue": sale.revenue,
                "sales_number": sale.sales_number,
                "date": sale.date.isoformat(),
                "user_id": sale.user.id,
            }
        ]
        assert response.status_code == status.HTTP_200_OK
        assert response_data == expected_response

    def test_bulk_create_sales_for_current_user(self, api_client):
        user = UserFactory(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@test.com",
            gender=User.MALE,
            age=30,
        )
        client = api_client()
        client.force_authenticate(user=user)

        bulk_create_data = {
            "sales_data": [
                {
                    "id": 1,
                    "date": "2021-4-17",
                    "product": "JBL Speakers",
                    "sales_number": 1,
                    "revenue": 0.5,
                    "user_id": user.id,
                },
                {
                    "id": 2,
                    "date": "2021-4-16",
                    "product": "ASUS Monitor",
                    "sales_number": 2,
                    "revenue": 3,
                    "user_id": user.id,
                },
            ],
        }

        response = client.post(
            self.endpoint,
            content_type="application/json",
            data=json.dumps(bulk_create_data),
        )
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert Sale.objects.filter(user=user).count() == 2


class TestSaleStatisticsAPI:
    endpoint = "/api/v1/sale_statistics/"

    def test_sale_stats_for_current_user(self, api_client):
        user = UserFactory(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@test.com",
            gender=User.MALE,
            age=30,
        )
        today = timezone.now().date()
        s1 = SaleFactory(
            user=user,
            date=today,
            product="Ketchup",
            sales_number=10,
            revenue=10,
        )
        s2 = SaleFactory(
            user=user,
            date=today,
            product="Ketchup",
            sales_number=20,
            revenue=20,
        )
        s3 = SaleFactory(
            user=user,
            date=today,
            product="Ketchup",
            sales_number=30,
            revenue=30,
        )
        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(self.endpoint)
        response_data = json.loads(response.content)

        expected_average_sale_all_user = 20.0
        expected_average_sales_for_current_user = 20.0
        expected_highest_revenue_sale_for_current_user = {
            "revenue": 30.0,
            "sale_id": s3.id,
        }
        assert response.status_code == status.HTTP_200_OK
        assert response_data["average_sale_all_user"] == expected_average_sale_all_user
        assert (
            response_data["average_sales_for_current_user"]
            == expected_average_sales_for_current_user
        )
        assert (
            response_data["highest_revenue_sale_for_current_user"]
            == expected_highest_revenue_sale_for_current_user
        )
