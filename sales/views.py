from braces import views
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, View

from users.models import User

from .forms import AddSalesForUserForm, SaleCSVForm


class ClearUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        num_deleted, _ = user.sales.all().delete()
        messages.success(request, f'{num_deleted} Sale object/s deleted for {user.email}.')
        return HttpResponseRedirect(user.get_absolute_url())


class AddUserSalesView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = SaleCSVForm(request.POST)

        if form.is_valid():
            sale_created_count = form.save(user=user)
            messages.success(request, f'{sale_created_count} Sale for user {user.email} created.')
        else:
            messages.error(request, 'Invalid CSV input. Please check your data.')

        return HttpResponseRedirect(user.get_absolute_url())


class ProductInfoInputPage(
    views.LoginRequiredMixin, views.SuperuserRequiredMixin, FormView
):
    template_name = "product_info_input.html"
    form_class = AddSalesForUserForm

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        sale_created_count = form.save(user)
        messages.success(self.request, f'{sale_created_count} Sale for user {user.email} created.')

        return HttpResponseRedirect(user.get_absolute_url())
