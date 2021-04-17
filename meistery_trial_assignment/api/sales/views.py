from collections import Counter
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from sales.models import Sale
from rest_framework import status

from rest_framework.response import Response
from .serializers import SaleSerializer
from django.db.models import Sum


class SaleViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        bulk_data = request.data.get("sales_data")
        bulk = isinstance(bulk_data, list)

        # TODO: add another ID field for "id" in bulk create?
        if not bulk:
            return super().create(request, *args, **kwargs)

        for data in bulk_data:
            data["user"] = request.user.id

        serializer = self.get_serializer(data=bulk_data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SaleStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        total_revenue_for_user = user.sale_set.aggregate(total_revenue=Sum("revenue"))[
            "total_revenue"
        ]
        total_sales_for_user = user.sale_set.count()
        average_sales_for_current_user = total_revenue_for_user / total_sales_for_user

        total_revenue = Sale.objects.aggregate(total_revenue=Sum("revenue"))[
            "total_revenue"
        ]
        total_sales = Sale.objects.count()
        average_sale_all_user = total_revenue / total_sales

        highest_revenue_sale_for_current_user = user.sale_set.order_by(
            "-revenue"
        ).first()

        products_sold_by_user = user.sale_set.values_list("product", flat=True)

        # TODO
        product_highest_revenue_for_current_user = 0
        product_highest_sales_number_for_current_user = 0

        return Response(
            {
                "average_sales_for_current_user": average_sales_for_current_user,
                "average_sale_all_user": average_sale_all_user,
                "highest_revenue_sale_for_current_user": {
                    "sale_id": highest_revenue_sale_for_current_user.id,
                    "revenue": highest_revenue_sale_for_current_user.revenue,
                },
                "product_highest_revenue_for_current_user": {
                    "product_name": "TBD",
                    "price": 0,
                },
                "product_highest_sales_number_for_current_user": {
                    "product_name:": "TBD",
                    "price": 0,
                },
            },
            status=status.HTTP_200_OK,
        )
