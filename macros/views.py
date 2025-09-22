from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FoodEntryForm, MacroSettingsForm
from .models import FoodEntry, MacroSettings


@login_required
def dashboard(request):
    today = date.today()
    settings_obj, _ = MacroSettings.objects.get_or_create(user=request.user)
    entries = FoodEntry.objects.filter(user=request.user, eaten_at=today).order_by("-created_at")
    totals = entries.aggregate(
        total_protein=Sum("protein_g"),
        total_carbs=Sum("carbs_g"),
        total_fats=Sum("fats_g"),
        total_calories=Sum("calories"),
    )

    # Coalesce totals to zero
    totals_coalesced = {
        "total_protein": totals.get("total_protein") or Decimal("0"),
        "total_carbs": totals.get("total_carbs") or Decimal("0"),
        "total_fats": totals.get("total_fats") or Decimal("0"),
        "total_calories": totals.get("total_calories") or Decimal("0"),
    }

    # Compute remaining targets for today (clamped at zero)
    remaining = {
        "protein_g": max(Decimal(settings_obj.daily_protein_g) - totals_coalesced["total_protein"], Decimal("0")),
        "carbs_g": max(Decimal(settings_obj.daily_carbs_g) - totals_coalesced["total_carbs"], Decimal("0")),
        "fats_g": max(Decimal(settings_obj.daily_fats_g) - totals_coalesced["total_fats"], Decimal("0")),
        "calories": max(Decimal(settings_obj.daily_calories) - totals_coalesced["total_calories"], Decimal("0")),
    }

    form = FoodEntryForm()
    if request.method == "POST":
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            food: FoodEntry = form.save(commit=False)
            food.user = request.user
            food.save()
            messages.success(request, "Food entry added.")
            return redirect("macros:dashboard")

    context = {
        "settings": settings_obj,
        "entries": entries,
        "totals": totals_coalesced,
        "remaining": remaining,
        "form": form,
        "today": today,
    }
    return render(request, "macros/dashboard.html", context)


@login_required
def settings_view(request):
    settings_obj, _ = MacroSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = MacroSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Macro settings updated.")
            return redirect("macros:dashboard")
    else:
        form = MacroSettingsForm(instance=settings_obj)
    return render(request, "macros/settings.html", {"form": form})


@login_required
def history(request):
    # Group totals by day for the current user
    daily_totals = (
        FoodEntry.objects.filter(user=request.user)
        .values("eaten_at")
        .annotate(
            total_protein=Sum("protein_g"),
            total_carbs=Sum("carbs_g"),
            total_fats=Sum("fats_g"),
            total_calories=Sum("calories"),
        )
        .order_by("-eaten_at")
    )
    return render(request, "macros/history.html", {"days": daily_totals})


@login_required
def day_detail(request, year: int, month: int, day: int):
    target = date(year, month, day)
    entries = FoodEntry.objects.filter(user=request.user, eaten_at=target).order_by("-created_at")
    settings_obj, _ = MacroSettings.objects.get_or_create(user=request.user)
    totals = entries.aggregate(
        total_protein=Sum("protein_g"),
        total_carbs=Sum("carbs_g"),
        total_fats=Sum("fats_g"),
        total_calories=Sum("calories"),
    )
    return render(
        request,
        "macros/day_detail.html",
        {"entries": entries, "settings": settings_obj, "totals": totals, "target": target},
    )


@login_required
def reset_today(request):
    if request.method == "POST":
        FoodEntry.objects.filter(user=request.user, eaten_at=date.today()).delete()
        messages.info(request, "Today's entries were reset.")
        return redirect("macros:dashboard")
    return render(request, "macros/reset_confirm.html")

# Create your views here.
