from django.contrib import admin

from content.models import Content
# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Content._meta.fields]
    search_fields = ["title"]
