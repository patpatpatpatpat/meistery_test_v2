from braces import views
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, View

from users.models import User

from .forms import AddSalesForUserForm, SaleCSVForm, SaleForm


class ClearUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.sales.all().delete()
        return HttpResponseRedirect(user.get_absolute_url())


class AddUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = SaleCSVForm(request.POST)

        if form.is_valid():
            sales_data = form.cleaned_data["csv"].split("\n")
            sales_data = sales_data[1:]  # Exclude column names

            for sale_data in sales_data:
                date, product, sales_number, revenue = sale_data.strip().split(",")
                as_dict = {
                    "date": date,
                    "product": product,
                    "sales_number": sales_number,
                    "revenue": revenue,
                    "user": user,
                }
                form = SaleForm(as_dict)

                if form.is_valid():
                    form.save()

        # TODO: do something if form is not valid
        return HttpResponseRedirect(user.get_absolute_url())


class ProductInfoInputPage(
    views.LoginRequiredMixin, views.SuperuserRequiredMixin, FormView
):
    template_name = "product_info_input.html"
    form_class = AddSalesForUserForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]

        sales_data = form.cleaned_data["csv"].split("\n")
        sales_data = sales_data[1:]  # Exclude column names

        for sale_data in sales_data:
            date, product, sales_number, revenue = sale_data.strip().split(",")
            as_dict = {
                "date": date,
                "product": product,
                "sales_number": sales_number,
                "revenue": revenue,
                "user": user,
            }
            form = SaleForm(as_dict)

            if form.is_valid():
                form.save()

        return HttpResponseRedirect(user.get_absolute_url())
