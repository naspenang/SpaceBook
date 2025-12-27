# website/admin.py
from django.contrib import admin
from .models import Branch, Campus


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "location")
    search_fields = ("code", "name")
    ordering = ("name",)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("campus_code", "branch", "campus_name", "role")
    ordering = ("branch__name", "campus_name")
    list_filter = ("branch", "role")
    search_fields = ("campus_code", "campus_name", "branch__name")


