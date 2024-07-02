from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class AccountAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        )
    list_display_links = ('email', 'username', 'first_name', )
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Contact Info', {'fields': ('phone_number',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('password', 'last_login', 'date_joined')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',
                       'first_name', 'last_name', 'phone_number',
                       'is_active', 'is_superuser', 'is_staff'),
        }),
    )


admin.site.register(models.Account, AccountAdmin)
