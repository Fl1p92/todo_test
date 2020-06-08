from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.tasks.models import Task
from .models import User, Address, Company, Coordinates


class AddressInline(admin.TabularInline):
    model = Address


class TasksInline(admin.TabularInline):
    model = Task
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'is_staff', 'website', 'company')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'company')
    search_fields = ('username', 'name', 'email', 'company')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'phone', 'website', 'company')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [AddressInline, TasksInline]


class CoordinatesInline(admin.TabularInline):
    model = Coordinates


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    inlines = [CoordinatesInline]


admin.site.register(Company)
