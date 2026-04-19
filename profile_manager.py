import re
from account_store import AccountStore

# ──────────────────// Profile Manager
class ProfileManager(AccountStore):

    def update_profile(self, account_number, name=None, email=None, phone=None):
        acc = self._get_account(account_number)
        if not acc:
            return "Account not found."

# ──────────────────// Validate and update fields
        if name is not None:
            if len(name.strip()) < 2:
                return "Name must be at least 2 characters."
            acc["name"] = name.strip()

# ───────────────────// Validate email
        if email is not None:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return "Invalid email format."
            for num, other in self.accounts.items():
                if num != account_number and other.get("email") == email:
                    return "Email is already in use by another account."
            acc["email"] = email.strip()

# ──────────────────// Validate phone number
        if phone is not None:
            if not re.fullmatch(r"\d{10,15}", str(phone)):
                return "Phone number must be 10–15 digits."
            acc["phone"] = str(phone).strip()

        self._save(account_number)
        return "Profile updated successfully."