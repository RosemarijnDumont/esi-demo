
from enum import Enum

# Assuming a simple Account model for demonstration purposes.
# In a real application, this would interact with a database ORM.

class AccountType(Enum):
    PAID = "paid"
    TRIAL = "trial"
    FREE = "free"
    # Add other account types as necessary

class Account:
    def __init__(self, id, name, account_type: AccountType):
        self.id = id
        self.name = name
        self.account_type = account_type

    @staticmethod
    def get_by_id(account_id):
        # This is a placeholder. In a real application, this would fetch from a database.
        # For demonstration, we'll return a mock account.
        if account_id == "trial_acc_123":
            return Account("trial_acc_123", "Trial Account", AccountType.TRIAL)
        elif account_id == "paid_acc_456":
            return Account("paid_acc_456", "Paid Account", AccountType.PAID)
        elif account_id == "free_acc_789":
            return Account("free_acc_789", "Free Account", AccountType.FREE)
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "account_type": self.account_type.value
        }
