from django.urls import path
from . import views

urlpatterns = [
    path('github/callback/', views.github_oauth_callback, name='github_oauth_callback'),
    path('github/initiate/', views.initiate_github_oauth, name='initiate_github_oauth'),
]
