from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# TODO: remove username
@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = ("user_id", "username", "email", "role", "is_superuser", "is_staff", "is_active")
    search_fields = ["email", "first_name", "lastname"]

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "address", "city", "state", "country", "pincode")}),
        ("Permissions", {"fields": ("is_active", "is_superuser", "is_staff")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username","role", "password1", "password2")}
        ),
        ("Personal info", {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "phone", "address", "city", "state", "country", "pincode")}
        ),
        ("Permissions", {
            "classes": ("wide",),
            "fields": ("is_active", "is_superuser", "is_staff")}
        ),
    )