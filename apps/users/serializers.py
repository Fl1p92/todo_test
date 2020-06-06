from rest_framework import serializers

from .models import User, Address, Company, Coordinates


class CoordinatesSerializer(serializers.ModelSerializer):
    """
    The serializer represents coordinates information.
    """
    class Meta:
        model = Coordinates
        fields = ('lat', 'lng')


class CompanySerializer(serializers.ModelSerializer):
    """
    The serializer represents company information.
    """
    class Meta:
        model = Company
        fields = ('name', 'catchPhrase', 'bs')


class AddressSerializer(serializers.ModelSerializer):
    """
    The serializer represents address information.
    """
    geo = CoordinatesSerializer()

    class Meta:
        model = Address
        fields = ('street', 'suite', 'city', 'zipcode', 'geo')


class UserSerializer(serializers.ModelSerializer):
    """
    The serializer represents user information, which includes the address and company.
    """
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'address', 'phone', 'website',
                  'company')

    def create(self, validated_data):
        # Clean validated data for create user
        address_data = validated_data.pop('address')
        company_data = validated_data.pop('company')
        geo_data = address_data.pop('geo')

        # Create company and user
        company = Company.objects.create(**company_data)
        instance = super().create(validated_data)
        instance.company_id = company.id
        instance.save(update_fields=['company_id'])

        # Create address with coordinates
        address = Address.objects.create(**address_data, user=instance)
        Coordinates.objects.create(**geo_data, address=address)

        return instance
