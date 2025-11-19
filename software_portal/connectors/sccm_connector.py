import requests
import json

class SCCMConnector:
    """
    Connects to SCCM for automated software deployment.
    """
    def __init__(self, sccm_api_base_url, api_key):
        self.base_url = sccm_api_base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def deploy_software(self, software_package_id, target_device_id):
        """
        Initiates a software deployment in SCCM.
        """
        endpoint = f"{self.base_url}/deployments"
        payload = {
            "SoftwarePackageId": software_package_id,
            "TargetDeviceId": target_device_id
        }
        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error deploying software via SCCM: {e}")
            raise

    def get_deployment_status(self, deployment_id):
        """
        Retrieves the status of a software deployment in SCCM.
        """
        endpoint = f"{self.base_url}/deployments/{deployment_id}/status"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting SCCM deployment status: {e}")
            raise

    def cancel_deployment(self, deployment_id):
        """
        Cancels a software deployment in SCCM.
        """
        endpoint = f"{self.base_url}/deployments/{deployment_id}/cancel"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error cancelling SCCM deployment: {e}")
            raise