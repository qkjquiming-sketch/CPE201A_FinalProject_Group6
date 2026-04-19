from account_store import AccountStore

# ──────────────────// Statements
class Statements(AccountStore):

    def get_statements(self, account_number):
        """Returns (list_of_transactions, error_message).
        On success, error_message is None.
        On failure, list is None."""
        acc = self._get_account(account_number)
        if not acc:
            return None, "Account not found."
        return acc.get("statements", []), None