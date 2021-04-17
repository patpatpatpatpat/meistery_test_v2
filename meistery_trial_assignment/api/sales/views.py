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
        return self.request.user.sales.all()

    def create(self, request, *args, **kwargs):
        bulk_data = request.data.get("sales_data")
        bulk = isinstance(bulk_data, list)

        if not bulk:
            return super().create(request, *args, **kwargs)

        serializer = self.get_serializer(data=bulk_data, many=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SaleStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        total_revenue_for_user = user.sales.aggregate(total_revenue=Sum("revenue"))[
            "total_revenue"
        ]
        total_sales_for_user = user.sales.count()
        average_sales_for_current_user = total_revenue_for_user / total_sales_for_user

        total_revenue = Sale.objects.aggregate(total_revenue=Sum("revenue"))[
            "total_revenue"
        ]
        total_sales = Sale.objects.count()
        average_sale_all_user = total_revenue / total_sales

        highest_revenue_sale_for_current_user = user.sales.order_by(
            "-revenue"
        ).first()

        products_sold_by_user = user.sales.values_list("product", flat=True)

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
