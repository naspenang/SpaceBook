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
    list_display = ("campus_name", "branch_name", "state", "role")
    list_filter = ("state", "role")
    search_fields = ("campus_name", "branch_name")
    ordering = ("branch_name", "campus_name")
