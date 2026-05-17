from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Address, NewsletterSubscriber

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_active', 'is_staff', 'newsletter_subscribed']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'avatar', 'bio', 'date_of_birth', 'newsletter_subscribed')}),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'country', 'address_type', 'is_default']

@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_editable = ['is_active']
