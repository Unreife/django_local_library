from django.contrib import admin

from .models import FoodEntry, MacroSettings


@admin.register(MacroSettings)
class MacroSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_calories", "daily_protein_g", "daily_carbs_g", "daily_fats_g")


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "eaten_at", "calories", "protein_g", "carbs_g", "fats_g")
    list_filter = ("eaten_at", "user")
    search_fields = ("name",)

# Register your models here.
