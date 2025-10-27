from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import override_settings, modify_settings
from unittest.mock import patch, MagicMock

@override_settings(GITHUB_OAUTH_CLIENT_ID='test_client_id',
                   GITHUB_OAUTH_CLIENT_SECRET='test_client_secret',
                   GITHUB_DEFAULT_REDIRECT_URI='http://localhost:8000/api/oauth/github/callback/',
                   OAUTH_ALLOWED_REDIRECT_HOSTS=['localhost'])
@modify_settings(INSTALLED_APPS={'append': 'oauth_api'}) 
default_api.py:12: error: 