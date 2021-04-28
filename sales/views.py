
from braces import views
from django.views.generic import View
from django.shortcuts import get_object_or_404

from users.models import User
from .forms import SaleCSVForm, SaleForm

from django.http import HttpResponseRedirect


class ClearUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.sales.all().delete()
        return HttpResponseRedirect(user.get_absolute_url())


class AddUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        form = SaleCSVForm(request.POST)

        if form.is_valid():
            sales_data = form.cleaned_data['csv'].split('\n')
            sales_data = sales_data[1:]  # Exclude column names

            for sale_data in sales_data:
                date, product, sales_number, revenue = sale_data.strip().split(',')
                as_dict = {
                    'date': date,
                    'product': product,
                    'sales_number': sales_number,
                    'revenue': revenue,
                    'user': user,
                }
                form = SaleForm(as_dict)

                if form.is_valid():
                    form.save()

        # TODO: do something if form is not valid
        return HttpResponseRedirect(user.get_absolute_url())
