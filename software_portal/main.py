from software_portal.workflow_engine.software_request_state_machine import SoftwareRequestStateMachine
from software_portal.connectors.sccm_connector import SCCMConnector
from software_portal.connectors.jamf_connector import JamfConnector
from software_portal.connectors.intune_connector import IntuneConnector
from software_portal.license_management.license_manager import LicenseManager
from software_portal.notification_service.notifier import Notifier
from software_portal.audit_logging.audit_logger import AuditLogger
import time
import os

# --- Configuration (Example - In a real app, use environment variables or a config file) ---
# Connectors
SCCM_API_BASE_URL = os.getenv("SCCM_API_BASE_URL", "http://localhost:8080/sccm-api")
SCCM_API_KEY = os.getenv("SCCM_API_KEY", "your_sccm_api_key")

JAMF_API_BASE_URL = os.getenv("JAMF_API_BASE_URL", "http://localhost:8080/jamf-api")
JAMF_USERNAME = os.getenv("JAMF_USERNAME", "your_jamf_username")
JAMF_PASSWORD = os.getenv("JAMF_PASSWORD", "your_jamf_password")

INTUNE_TENANT_ID = os.getenv("INTUNE_TENANT_ID", "your_intune_tenant_id")
INTUNE_CLIENT_ID = os.getenv("INTUNE_CLIENT_ID", "your_intune_client_id")
INTUNE_CLIENT_SECRET = os.getenv("INTUNE_CLIENT_SECRET", "your_intune_client_secret")

# Notifier
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "noreply@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_smtp_password")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", None)
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL", None)

# --- Initialization ---
audit_logger = AuditLogger()
license_manager = LicenseManager()
notifier = Notifier(SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SLACK_WEBHOOK_URL, TEAMS_WEBHOOK_URL)
sccm_connector = SCCMConnector(SCCM_API_BASE_URL, SCCM_API_KEY)
jamf_connector = JamfConnector(JAMF_API_BASE_URL, JAMF_USERNAME, JAMF_PASSWORD)
intune_connector = IntuneConnector(INTUNE_TENANT_ID, INTUNE_CLIENT_ID, INTUNE_CLIENT_SECRET)

# In a real application, approved software would be stored in a database
APPROVED_SOFTWARE = {
    "microsoft_office": {"name": "Microsoft Office", "sccm_package_id": "MSOFFICE2019", "type": "sccm"},
    "adobe_creative_cloud": {"name": "Adobe Creative Cloud", "jamf_policy_name": "AdobeCCInstall", "type": "jamf"},
    "visual_studio_code": {"name": "Visual Studio Code", "intune_app_id": "VSCODEINTUNE", "type": "intune"}
}

class SoftwareRequestProcessor:
    """
    Manages the end-to-end processing of a software request.
    """
    def __init__(self, request_id, requester_id, software_key, target_device_id, approval_group_email):
        self.request_id = request_id
        self.requester_id = requester_id
        self.software_key = software_key
        self.target_device_id = target_device_id
        self.approval_group_email = approval_group_email
        self.state_machine = SoftwareRequestStateMachine()
        self.software_info = APPROVED_SOFTWARE.get(software_key)
        if not self.software_info:
            raise ValueError(f"Software with key '{software_key}' is not approved or does not exist.")

        audit_logger.log("SOFTWARE_REQUEST_INITIATED", self.requester_id, self.request_id, 
                         {"software": self.software_info["name"], "device": self.target_device_id})

    def process_request(self):
        """
        Orchestrates the software request lifecycle.
        """
        try:
            # 1. Request -> Pending Approval
            self.state_machine.request(self.request_id)
            self._notify_for_approval()

            # --- Simulate Approval Logic (would be an external action) ---
            print(f"\n--- Waiting for approval for request {self.request_id} ---")
            is_approved = self._await_approval(self.request_id) 

            if is_approved:
                # 2. Pending Approval -> Approved
                self.state_machine.approve(self.request_id)
                audit_logger.log("SOFTWARE_REQUEST_APPROVED", "admin_user", self.request_id)
                notifier.send_email(self.requester_id, f"Software Request {self.request_id} Approved", 
                                    f"Your request for {self.software_info['name']} has been approved.")

                # 3. Approved -> License Assigned
                license_id = license_manager.assign_license(self.software_info["name"], self.requester_id)
                self.state_machine.assign_license(self.request_id, license_id)
                audit_logger.log("LICENSE_ASSIGNED", "system", self.request_id, {"license_id": license_id})

                # 4. License Assigned -> Installation In Progress
                self.state_machine.start_installation(self.request_id)
                self._execute_installation()

                # 5. Installation In Progress -> Completed
                self.state_machine.complete_installation(self.request_id)
                audit_logger.log("SOFTWARE_INSTALLED", "system", self.request_id)
                notifier.send_email(self.requester_id, f"Software Installation {self.request_id} Complete",
                                    f"The installation of {self.software_info['name']} on your device is complete.")
            else:
                # 2. Pending Approval -> Rejected
                reason = "Manual rejection by administrator."
                self.state_machine.reject(self.request_id, reason)
                audit_logger.log("SOFTWARE_REQUEST_REJECTED", "admin_user", self.request_id, {"reason": reason})
                notifier.send_email(self.requester_id, f"Software Request {self.request_id} Rejected",
                                    f"Your request for {self.software_info['name']} has been rejected. Reason: {reason}")


        except Exception as e:
            print(f"An error occurred during request processing for {self.request_id}: {e}")
            self.state_machine.fail_installation(self.request_id, str(e))
            audit_logger.log("SOFTWARE_PROCESS_FAILED", "system", self.request_id, {"error": str(e)})
            notifier.send_email(self.requester_id, f"Software Request {self.request_id} Failed",
                                f"There was an error processing your request for {self.software_info['name']}. Please contact IT.")
            self._handle_failed_installation()

    def _notify_for_approval(self):
        """
        Sends a notification to the approval group.
        """
        subject = f"New Software Approval Request: {self.software_info['name']} for {self.requester_id}"
        body = f"A new software request for {self.software_info['name']} by {self.requester_id} (device: {self.target_device_id}) is pending your approval. Request ID: {self.request_id}"
        notifier.send_email(self.approval_group_email, subject, body)
        notifier.send_slack_message(f"New software request for *{self.software_info['name']}* by <@{self.requester_id}>. Request ID: `{self.request_id}`", channel="#software-approvals")
        audit_logger.log("APPROVAL_NOTIFICATION_SENT", "system", self.request_id, {"recipient": self.approval_group_email})

    def _await_approval(self, request_id):
        """
        Simulates waiting for external approval. In a real system, this would involve a callback
        from an approval portal or a polling mechanism.
        """
        # For demonstration, we'll simulate an approval after a short delay.
        # In a real system, this would be an API call to an approval system that the admin interacts with.
        time.sleep(3) 
        print(f"Simulating approval for request {request_id}...")
        return True # Assume approved for now

    def _execute_installation(self):
        """
        Executes the software installation using the appropriate connector.
        """
        install_type = self.software_info["type"]
        software_name = self.software_info["name"]

        try:
            if install_type == "sccm":
                print(f"Initiating SCCM deployment for {software_name}...")
                sccm_connector.deploy_software(self.software_info["sccm_package_id"], self.target_device_id)
                audit_logger.log("SCCM_DEPLOYMENT_INITIATED", "system", self.request_id, 
                                 {"software": software_name, "device": self.target_device_id})
                # In a real scenario, you'd poll SCCM for deployment status

            elif install_type == "jamf":
                print(f"Initiating Jamf policy application for {software_name}...")
                jamf_connector.apply_software_policy(self.software_info["jamf_policy_name"], self.target_device_id)
                audit_logger.log("JAMF_POLICY_APPLIED", "system", self.request_id,
                                 {"software": software_name, "device": self.target_device_id})
                # In a real scenario, you'd poll Jamf for device compliance/policy status

            elif install_type == "intune":
                print(f"Initiating Intune application assignment for {software_name}...")
                intune_connector.assign_application_to_user(self.software_info["intune_app_id"], self.requester_id) # Assuming user_id for Intune assignment
                audit_logger.log("INTUNE_APP_ASSIGNED", "system", self.request_id,
                                 {"software": software_name, "user": self.requester_id})
                # In a real scenario, you'd poll Intune/Graph API for application installation status

            else:
                raise ValueError(f"Unknown installation type: {install_type}")

        except Exception as e:
            error_msg = f"Failed to execute installation for {software_name} via {install_type}: {e}"
            print(error_msg)
            raise RuntimeError(error_msg)

    def _handle_failed_installation(self):
        """
        Implements rollback/retry logic for failed installations.
        """
        print(f"Handling failed installation for request {self.request_id}. Current state: {self.state_machine.current_state.id}")
        # For demonstration, we'll offer a retry. In production, this might involve more sophisticated logic.
        if self.state_machine.current_state.id == "failed":
            print("Attempting to retry installation...")
            audit_logger.log("INSTALLATION_RETRY_ATTEMPT", "system", self.request_id)
            try:
                self.state_machine.retry_installation(self.request_id)
                self._execute_installation() # Re-attempt installation
                self.state_machine.complete_installation(self.request_id)
                audit_logger.log("SOFTWARE_INSTALLED_RETRY_SUCCESS", "system", self.request_id)
                notifier.send_email(self.requester_id, f"Software Installation {self.request_id} Retried and Complete",
                                    f"The installation of {self.software_info['name']} on your device was retried and is now complete.")
            except Exception as e:
                print(f"Retry failed for {self.request_id}: {e}")
                audit_logger.log("INSTALLATION_RETRY_FAILED", "system", self.request_id, {"error": str(e)})
                notifier.send_email(self.requester_id, f"Software Installation {self.request_id} Retry Failed",
                                    f"The retry for installing {self.software_info['name']} on your device also failed. Please contact IT.")

# --- Example Usage ---
if __name__ == "__main__":
    # Simulate a user request
    print("\n--- Initiating Software Request 1 ---")
    request1 = SoftwareRequestProcessor(
        request_id="req_001",
        requester_id="user@example.com",
        software_key="microsoft_office",
        target_device_id="device_abc_123",
        approval_group_email="it-approvals@example.com"
    )
    request1.process_request()

    print("\n--- Initiating Software Request 2 ---")
    request2 = SoftwareRequestProcessor(
        request_id="req_002",
        requester_id="newhire@example.com",
        software_key="adobe_creative_cloud",
        target_device_id="mac_def_456",
        approval_group_email="it-approvals@example.com"
    )
    request2.process_request()

    print("\n--- Initiating Software Request 3 (Simulated Failure and Retry) ---")
    # To simulate a failure, you'd modify _execute_installation or a connector temporarily.
    # For this example, let's assume `_await_approval` could return False sometimes.
    # We'll re-run request1 to see the retry logic if it hits a failure point.
    
    # Let's explicitly try to cause a failure for demonstration by introducing a bad software key
    try:
        request_fail = SoftwareRequestProcessor(
            request_id="req_003",
            requester_id="failuser@example.com",
            software_key="non_existent_software", # This will cause an initial ValueError
            target_device_id="pc_fail_789",
            approval_group_email="it-approvals@example.com"
        )
        request_fail.process_request()
    except ValueError as e:
        print(f"Caught expected error for bad software key: {e}")
        audit_logger.log("SOFTWARE_REQUEST_INVALID", "failuser@example.com", "req_003", {"error": str(e)})

    # Display some audit logs
    print("\n--- Recent Audit Logs ---")
    for log_entry in audit_logger.get_logs(limit=5):
        print(log_entry)

    # Display license status
    print("\n--- License Status for Microsoft Office ---")
    print(f"Available Microsoft Office licenses: {license_manager.get_available_licenses('Microsoft Office')}")
    print("\n--- License Status for Adobe Creative Cloud ---")
    print(f"Available Adobe Creative Cloud licenses: {license_manager.get_available_licenses('Adobe Creative Cloud')}")