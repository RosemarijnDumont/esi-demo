from django.urls import path
from . import views

urlpatterns = [
    path('trial_accounts/<int:account_id>/configure_sso/', views.configure_trial_sso, name='configure_trial_sso'),
    # Other URLs
]