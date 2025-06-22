from django.urls import path
from .views import calculate_investment, buffet_analysis

urlpatterns = [
    path("calculate/", calculate_investment),
    path("buffet-analysis/", buffet_analysis),
]

