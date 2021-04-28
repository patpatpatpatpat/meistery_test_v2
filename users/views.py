from django.shortcuts import render

from django.views.generic import FormView, CreateView, TemplateView, DetailView
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User
from braces import views
from sales.forms import SaleCSVForm, SaleForm


class CreateUserView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, CreateView):
    template_name = 'create_user.html'
    form_class = UserForm


class EditUserView(views.LoginRequiredMixin, views.SuperuserRequiredMixin, DetailView):
    template_name = 'edit_user.html'
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edit_user_form = UserForm(instance=self.get_object())

        context['user_form'] = edit_user_form
        context['sale_csv_form'] = SaleCSVForm()
        return context

    def post(self, request, *args, **kwargs):
        edit_user_form = UserForm(request.POST, instance=self.get_object())

        if edit_user_form.is_valid():
            edit_user_form.save()
            return HttpResponseRedirect(self.get_object().get_absolute_url())
        else:
            context = {}
            context['user_form'] = edit_user_form
            context['sale_csv_form'] = SaleCSVForm()
            context['user'] = self.get_object()
            return self.render_to_response(context)
