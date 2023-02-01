from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, StripeCustomer

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Membership status', {
            'fields': ('is_member', 'is_unlimited')
        }),
    )
    list_display = ['email', 'username', 'is_member', 'is_unlimited']
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StripeCustomer)