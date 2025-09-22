from django import forms
from .models import MacroSettings, FoodEntry


class MacroSettingsForm(forms.ModelForm):
    class Meta:
        model = MacroSettings
        fields = [
            "daily_protein_g",
            "daily_carbs_g",
            "daily_fats_g",
        ]


class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodEntry
        fields = ["name", "protein_g", "carbs_g", "fats_g"]


