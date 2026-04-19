from account_store import AccountStore

# ──────────────────// Withdrawal
class Withdrawal(AccountStore):

    def withdraw(self, account_number, amount):
        acc = self._get_account(account_number)
        if not acc:
            return "Account not found."
        if acc["status"] != "active":
            return "Account is not active."
        if amount <= 0:
            return "Withdrawal amount must be greater than zero."
        if amount > acc["balance"]:
            return f"Insufficient balance. Current balance: ₱{acc['balance']:,.2f}"

        acc["balance"] -= round(amount, 2)
        self._log_transaction(account_number, "Withdrawal", amount,
                              note=f"Withdrew ₱{amount:,.2f}")
        return f"Withdrawal successful. New balance: ₱{acc['balance']:,.2f}"