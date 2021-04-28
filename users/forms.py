from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "gender",
            "age",
            "is_staff",
            "is_superuser",
            "is_active",
            "country",
            "city",
        )

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        country = cleaned_data.get("country")

        if city and country:
            if not country.cities.filter(id=city.id).exists():
                self.add_error("city", f"{city.name} is not under {country.name}")
