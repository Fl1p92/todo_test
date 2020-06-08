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
        address_data = validated_data.pop('address', {})
        company_data = validated_data.pop('company', None)
        geo_data = address_data.pop('geo', None)

        # Create user and company
        instance = super().create(validated_data)
        if company_data is not None:
            company = Company.objects.create(**company_data)
            instance.company_id = company.id
            instance.save(update_fields=['company_id'])

        # Create address with coordinates
        if address_data:
            address = Address.objects.create(**address_data, user=instance)
            if geo_data is not None:
                Coordinates.objects.create(**geo_data, address=address)

        return instance

    def update(self, instance, validated_data):
        # Clean validated data for update user
        address_data = validated_data.pop('address', {})
        company_data = validated_data.pop('company', None)
        geo_data = address_data.pop('geo', None)

        # Update user and company
        instance = super().update(instance, validated_data)
        if company_data is not None:
            Company.objects.filter(id=instance.company_id).update(**company_data)

        # Update address with coordinates
        if address_data:
            Address.objects.filter(user=instance).update(**address_data)
            if geo_data is not None:
                Coordinates.objects.filter(address__user=instance).update(**geo_data)

        return instance
