from rest_framework import serializers

from users.models import City, Country, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "age",
            "country",
            "city",
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(source="city_set", many=True, required=False)

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "cities",
        )
