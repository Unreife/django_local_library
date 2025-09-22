from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP


User = get_user_model()


class MacroSettings(models.Model):
    """Per-user macro targets. One row per user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="macro_settings")
    daily_calories = models.PositiveIntegerField(default=2000)
    daily_protein_g = models.PositiveIntegerField(default=150)
    daily_carbs_g = models.PositiveIntegerField(default=200)
    daily_fats_g = models.PositiveIntegerField(default=70)

    def __str__(self) -> str:
        return f"MacroSettings({self.user})"

    def save(self, *args, **kwargs):
        # Auto-calculate daily calories from macro grams
        protein_cals = Decimal(self.daily_protein_g or 0) * Decimal(4)
        carbs_cals = Decimal(self.daily_carbs_g or 0) * Decimal(4)
        fats_cals = Decimal(self.daily_fats_g or 0) * Decimal(9)
        total = protein_cals + carbs_cals + fats_cals
        self.daily_calories = int(total.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        super().save(*args, **kwargs)


class FoodEntry(models.Model):
    """A single food log entry for a user and date."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_entries")
    name = models.CharField(max_length=200)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carbs_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fats_g = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    calories = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    eaten_at = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-eaten_at", "-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.eaten_at})"

    def save(self, *args, **kwargs):
        # Auto-calculate calories from macros
        protein_cals = (self.protein_g or 0) * Decimal(4)
        carbs_cals = (self.carbs_g or 0) * Decimal(4)
        fats_cals = (self.fats_g or 0) * Decimal(9)
        total = Decimal(protein_cals) + Decimal(carbs_cals) + Decimal(fats_cals)
        self.calories = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super().save(*args, **kwargs)

# Create your models here.
