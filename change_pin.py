import re
from account_store import AccountStore

# ──────────────────// Change PIN
class ChangePin(AccountStore):
    
    def change_pin(self, account_number, old_pin, new_pin):
        acc = self._get_account(account_number)
        if not acc:
            return "Account not found."
        if acc["pin_code"] != self._hash(old_pin):
            return "Incorrect current PIN."
        if not re.fullmatch(r"\d{6}", str(new_pin)):
            return "New PIN must be exactly 6 digits."
        if self._hash(new_pin) == acc["pin_code"]:
            return "New PIN must be different from the current PIN."

        acc["pin_code"] = self._hash(new_pin)
        self._save(account_number)
        return "PIN changed successfully."