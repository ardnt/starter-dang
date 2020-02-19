from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db.models import Case, Value, When

from .forms import EmailUserCreationForm, EmailUserChangeForm


def toggle_active_action(modeladmin, request, queryset):
    queryset.update(
        is_active=Case(When(is_active=True, then=Value(False)), default=Value(True))
    )


toggle_active_action.short_description = 'Toggle active status'


@admin.register(get_user_model())
class EmailUserAdmin(UserAdmin):
    add_form = EmailUserCreationForm
    form = EmailUserChangeForm

    actions = (toggle_active_action,)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email',)}),)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'remote_id')}),
        (
            'Permissions',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')},
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups', {'fields': ('groups',)}),
    )
    list_display = ('email', 'id', 'name', 'is_active', 'is_staff', 'last_login')
    ordering = ('email',)
    search_fields = ('email', 'name')
