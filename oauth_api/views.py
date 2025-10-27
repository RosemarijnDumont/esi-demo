import logging
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from urllib.parse import urlparse
import time

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def github_oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    redirect_uri = request.GET.get('redirect_uri')

    logger.info(f"OAuth Callback Initiated: code={code}, state={state}, redirect_uri={redirect_uri}")

    if not code:
        logger.error("OAuth Callback Error: 'code' not found in request.")
        return Response({'error': 'Authorization code not provided.'}, status=status.HTTP_400_BAD_REQUEST)

    if not redirect_uri:
        logger.error("OAuth Callback Error: 'redirect_uri' not found in request.")
        return Response({'error': 'Redirect URI not provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate and sanitize redirect URI
    parsed_redirect_uri = urlparse(redirect_uri)
    allowed_redirect_hosts = getattr(settings, 'OAUTH_ALLOWED_REDIRECT_HOSTS', [])
    if parsed_redirect_uri.hostname not in allowed_redirect_hosts:
        logger.error(f"OAuth Callback Error: Invalid redirect URI host: {parsed_redirect_uri.hostname}")
        return Response({'error': 'Invalid redirect URI.'}, status=status.HTTP_400_BAD_REQUEST)

    if state != request.session.get('oauth_state'):
        logger.error(f"OAuth Callback Error: State mismatch. Expected: {request.session.get('oauth_state')}, Received: {state}")
        return Response({'error': 'State mismatch.'}, status=status.HTTP_400_BAD_REQUEST)

    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        'client_id': settings.GITHUB_OAUTH_CLIENT_ID,
        'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri,
        'state': state,
    }
    headers = {'Accept': 'application/json'}

    retries = 3
    for i in range(retries):
        try:
            logger.info(f"Attempt {i+1} to exchange code for token with GitHub. Payload: {payload}")
            response = requests.post(token_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            token_data = response.json()
            logger.info(f"Successfully exchanged code for token. Response: {token_data}")
            break
        except requests.exceptions.Timeout:
            logger.error(f"OAuth Token Exchange Error: Request timed out on attempt {i+1}.")
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
                continue
            return Response({'error': 'OAuth token exchange timed out after multiple retries.'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.exceptions.RequestException as e:
            logger.error(f"OAuth Token Exchange Error: {e}. Response: {response.text if response else 'No response'}")
            if i < retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
                continue
            return Response({'error': f'Failed to exchange code for token: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        logger.error("OAuth Token Exchange Error: Failed after multiple retries.")
        return Response({'error': 'Failed to exchange code for token after multiple retries.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    access_token = token_data.get('access_token')
    if not access_token:
        logger.error(f"OAuth Token Exchange Error: 'access_token' not found in response. Token Data: {token_data}")
        return Response({'error': 'Access token not received.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # In a real application, you would now use this access_token to fetch user data
    # and create/link the user account in your system.
    # For this example, we'll just return the access token.
    return Response({'message': 'OAuth callback successful', 'access_token': access_token})


@api_view(['GET'])
@permission_classes([AllowAny])
def initiate_github_oauth(request):
    client_id = settings.GITHUB_OAUTH_CLIENT_ID
    redirect_uri = request.GET.get('redirect_uri', getattr(settings, 'GITHUB_DEFAULT_REDIRECT_URI', ''))
    scope = 'user:email'
    
    # Generate a secure state token and store it in the session
    import os
    state = os.urandom(16).hex()
    request.session['oauth_state'] = state
    
    auth_url = (
        f"https://github.com/login/oauth/authorize?" +
        f"client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
    )
    logger.info(f"Initiating GitHub OAuth: auth_url={auth_url}")
    return Response({'auth_url': auth_url})
