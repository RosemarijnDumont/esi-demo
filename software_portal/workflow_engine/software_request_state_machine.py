from statemachine import StateMachine, State

class SoftwareRequestStateMachine(StateMachine):
    """
    Defines the states and transitions for a software request.
    """
    requested = State(initial=True)
    pending_approval = State()
    approved = State()
    license_assigned = State()
    installation_in_progress = State()
    completed = State()
    rejected = State()
    failed = State()
    cancelled = State()

    request = requested.to(pending_approval)
    approve = pending_approval.to(approved)
    reject = pending_approval.to(rejected)
    assign_license = approved.to(license_assigned)
    start_installation = license_assigned.to(installation_in_progress)
    complete_installation = installation_in_progress.to(completed)
    fail_installation = installation_in_progress.to(failed)
    retry_installation = failed.to(installation_in_progress)
    cancel_request = (requested | pending_approval | approved | license_assigned | failed).to(cancelled)

    def on_enter_pending_approval(self, request_id):
        print(f"Software request {request_id} is pending approval.")
        # Trigger notification to approvers

    def on_enter_approved(self, request_id):
        print(f"Software request {request_id} has been approved.")
        # Trigger license assignment process

    def on_enter_rejected(self, request_id, reason):
        print(f"Software request {request_id} has been rejected. Reason: {reason}")
        # Trigger notification to user

    def on_enter_license_assigned(self, request_id, license_details):
        print(f"Software request {request_id} has been assigned a license: {license_details}.")
        # Trigger installation process

    def on_enter_installation_in_progress(self, request_id):
        print(f"Software installation for request {request_id} is in progress.")
        # Trigger installation tool

    def on_enter_completed(self, request_id):
        print(f"Software installation for request {request_id} has been completed successfully.")
        # Trigger notification to user, update audit log

    def on_enter_failed(self, request_id, error_message):
        print(f"Software installation for request {request_id} failed. Error: {error_message}")
        # Trigger notification to user and IT, update audit log

    def on_enter_cancelled(self, request_id):
        print(f"Software request {request_id} has been cancelled.")
        # Update audit log, clean up resources if any