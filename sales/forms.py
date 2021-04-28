from django import forms

from users.models import User

from .models import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (
            "date",
            "product",
            "sales_number",
            "revenue",
            "user",
        )


class SaleCSVForm(forms.Form):
    csv = forms.CharField(widget=forms.Textarea)


class AddSalesForUserForm(SaleCSVForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False, is_staff=False),
    )
