from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'gender',
            'age',
            'is_staff',
            'is_superuser',
            'is_active',
            'country',
            'city',
        )

    # TODO custom validation: city must be under country
