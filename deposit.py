from account_store import AccountStore

# ──────────────────// Deposit
class Deposit(AccountStore):

    def deposit(self, account_number, amount):
        acc = self._get_account(account_number)
        if not acc:
            return "Account not found."
        if acc["status"] != "active":
            return "Account is not active."
        if amount <= 0:
            return "Deposit amount must be greater than zero."

        acc["balance"] += round(amount, 2)
        self._log_transaction(account_number, "Deposit", amount,
                              note=f"Deposited ₱{amount:,.2f}")
        return f"Deposit successful. New balance: ₱{acc['balance']:,.2f}"