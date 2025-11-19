import requests
import json

class JamfConnector:
    """
    Connects to Jamf for automated software deployment.
    """
    def __init__(self, jamf_api_base_url, username, password):
        self.base_url = jamf_api_base_url
        self.auth = (username, password)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_software_policy(self, policy_name):
        """
        Retrieves a software policy by name from Jamf.
        """
        endpoint = f"{self.base_url}/JSSResource/policies/name/{policy_name}"
        try:
            response = requests.get(endpoint, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving Jamf policy '{policy_name}': {e}")
            raise

    def apply_software_policy(self, policy_id, target_device_id):
        """
        Applies a software policy to a target device in Jamf.
        Note: Jamf typically uses profiles or policies applied at a group level.
        This example assumes an endpoint for direct policy application to a device if available,
        or describes the logical step of assigning a device to a group that has the policy.
        """
        print(f"Applying Jamf policy {policy_id} to device {target_device_id} (simulated).")
        # In a real scenario, this would likely involve updating a computer record's group membership
        # or triggering a policy via Jamf Pro API that allows per-device execution if such an API exists.
        # For simplicity, we'll simulate a successful application here.
        return {"status": "success", "message": f"Policy {policy_id} applied to device {target_device_id}"}

    def get_device_status(self, device_id):
        """
        Retrieves the status of a device from Jamf (e.g., policy compliance).
        """
        endpoint = f"{self.base_url}/JSSResource/computers/id/{device_id}"
        try:
            response = requests.get(endpoint, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting Jamf device status for '{device_id}': {e}")
            raise