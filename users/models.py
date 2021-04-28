from django.db import models
from django.core import validators

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def get_admin_by_natural_key(self, username):
        return self.get(
            **{
                self.model.USERNAME_FIELD: username,
                "is_superuser": True,
            }
        )


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for Meistery Sales Processor."""

    MALE = "male"
    FEMALE = "female"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    first_name = models.CharField(_("First name"), blank=True, max_length=255)
    last_name = models.CharField(_("Last name"), blank=True, max_length=255)
    username = models.CharField(
        _("username"),
        max_length=254,
        unique=True,
        help_text=_(
            "Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$",
                _(
                    "Enter a valid username. This value may contain only "
                    "letters, numbers "
                    "and @/./+/-/_ characters."
                ),
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="users",
    )
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE, blank=True, null=True, related_name="users"
    )

    objects = CustomUserManager()
    REQUIRED_FIELDS = ["username", "age", "gender", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('edit_user', args=[self.id,])

class Country(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="cities",
    )

    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")

    def __str__(self):
        return f"{self.name}, {self.country}"
