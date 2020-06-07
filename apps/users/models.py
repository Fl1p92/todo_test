from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended User model with address information, company information and other additions.
    """
    name = models.CharField(max_length=150, blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    website = models.CharField(max_length=100, blank=True, default='')
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, related_name='users', blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'[{self.id}] {self.name}'


class Address(models.Model):
    """
    User address details.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Address'

    def __str__(self):
        return f"{self.user}'s address [{self.id}]"


class Coordinates(models.Model):
    """
    Latitude and Longitude coordinates.
    """
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='geo')

    class Meta:
        verbose_name_plural = 'Coordinates'


class Company(models.Model):
    """
    User company details.
    """
    name = models.CharField(max_length=100)
    catchPhrase = models.CharField(max_length=100)
    bs = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f'[{self.id}] {self.name}'
