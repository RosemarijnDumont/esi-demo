from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/oauth/', include('oauth_api.urls')), # Include OAuth API URLs
]
