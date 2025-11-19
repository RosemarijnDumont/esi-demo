import uuid
from datetime import datetime

class LicenseManager:
    """
    Manages the allocation and tracking of software licenses.
    """
    def __init__(self):
        self.licenses = {}
        self.software_license_pools = {
            "Microsoft Office": {"total": 100, "available": 50, "assigned": {}},
            "Adobe Creative Cloud": {"total": 20, "available": 10, "assigned": {}}
        }

    def assign_license(self, software_name, user_id):
        """
        Assigns an available license for the given software to a user.
        """
        if software_name not in self.software_license_pools:
            raise ValueError(f"Software '{software_name}' not managed by license manager.")

        pool = self.software_license_pools[software_name]
        if pool["available"] > 0:
            license_id = str(uuid.uuid4())
            assignment_date = datetime.now().isoformat()
            self.licenses[license_id] = {
                "software_name": software_name,
                "user_id": user_id,
                "assigned_date": assignment_date,
                "status": "assigned"
            }
            pool["available"] -= 1
            pool["assigned"][user_id] = license_id
            print(f"License {license_id} for {software_name} assigned to user {user_id}.")
            return license_id
        else:
            raise RuntimeError(f"No available licenses for {software_name}.")

    def revoke_license(self, license_id):
        """
        Revokes an assigned license and makes it available again.
        """\n        if license_id not in self.licenses:
            raise ValueError(f"License ID {license_id} not found.")

        license_info = self.licenses[license_id]
        software_name = license_info["software_name"]
        user_id = license_info["user_id"]

        if software_name in self.software_license_pools:
            pool = self.software_license_pools[software_name]
            if user_id in pool["assigned"] and pool["assigned"][user_id] == license_id:
                pool["available"] += 1
                del pool["assigned"][user_id]
                self.licenses[license_id]["status"] = "revoked"
                self.licenses[license_id]["revoked_date"] = datetime.now().isoformat()
                print(f"License {license_id} for {software_name} revoked from user {user_id}.")
                return True
        return False

    def get_license_status(self, license_id):
        """
        Retrieves the status of a specific license.
        """
        return self.licenses.get(license_id)

    def get_available_licenses(self, software_name):
        """
        Returns the number of available licenses for a given software.
        """\n        return self.software_license_pools.get(software_name, {}).get("available", 0)