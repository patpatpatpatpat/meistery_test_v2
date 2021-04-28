from django import forms

from users.models import User

from .models import Sale

EXPECTED_CSV_COLUMNS = {"date", "product", "sales_number", "revenue"}


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

    def clean_csv(self):
        data = self.cleaned_data["csv"].split("\n")
        columns_as_set = set(data[0].strip().split(","))

        has_expected_columns = EXPECTED_CSV_COLUMNS.difference(columns_as_set) == set()

        if not has_expected_columns:
            raise forms.ValidationError("Invalid CSV input.")

        return self.cleaned_data["csv"]

    def save(self, user):
        sales_data = self.cleaned_data["csv"].split("\n")
        sales_data = sales_data[1:]  # Exclude column names
        sale_created_count = 0

        for sale_data in sales_data:
            try:
                date, product, sales_number, revenue = sale_data.strip().split(",")
            except ValueError:
                continue

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
                sale_created_count += 1

        return sale_created_count


class AddSalesForUserForm(SaleCSVForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=False, is_staff=False),
    )
