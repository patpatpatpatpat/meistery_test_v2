from users.models import User, Country, City

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'email',
            'gender',
            'age',
            'country',
            'city',
            'first_name',
            'last_name',
        ]

    def update(self, instance, validated_data):
        validated_data['name'] = validated_data['first_name'] + ' ' + validated_data['last_name']
        instance = super().update(instance, validated_data)
        return instance


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name',
        )


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(source="city_set", many=True)

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'cities',
        )