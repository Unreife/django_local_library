from django.urls import path
from . import views


app_name = "macros"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("settings/", views.settings_view, name="settings"),
    path("history/", views.history, name="history"),
    path("day/<int:year>/<int:month>/<int:day>/", views.day_detail, name="day_detail"),
    path("reset-today/", views.reset_today, name="reset_today"),
]


