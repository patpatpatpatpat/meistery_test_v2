import factory

from meistery_trial_assignment.api.users.factories import UserFactory
from sales.models import Sale


class SaleFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    product = factory.Sequence(lambda n: f"product{n}")
    sales_number = 1
    revenue = 2

    class Meta:
        model = Sale
