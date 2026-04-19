from account_store import AccountStore

# ──────────────────// Change Password
class ChangePassword(AccountStore):

    def change_password(self, account_number, old_password, new_password):
        acc = self._get_account(account_number)
        if not acc:
            return "Account not found."
        if acc["password"] != self._hash(old_password):
            return "Incorrect current password."
        if len(new_password) < 8:
            return "New password must be at least 8 characters."
        if self._hash(new_password) == acc["password"]:
            return "New password must be different from the current password."

        acc["password"] = self._hash(new_password)
        self._save(account_number)
        return "Password changed successfully."