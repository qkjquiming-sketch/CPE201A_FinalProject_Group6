import re
from account_store import AccountStore

# ──────────────────// Transfer
class Transfer(AccountStore):

    def transfer(self, from_account, to_account_number, amount):
# ──────────────────// Validate inputs
        if not re.fullmatch(r"\d{12}", str(to_account_number)):
            return "Recipient account number must be exactly 12 digits."

# ──────────────────// Validate accounts and amount
        sender = self._get_account(from_account)
        if not sender:
            return "Sender account not found."
        if sender["status"] != "active":
            return "Your account is not active."

# ──────────────────// Validate recipient account
        receiver = self._get_account(to_account_number)
        if not receiver:
            return "Recipient account not found."
        if receiver["status"] != "active":
            return "Recipient account is not active."
        if from_account == to_account_number:
            return "Cannot transfer to the same account."
        if amount <= 0:
            return "Transfer amount must be greater than zero."
        if amount > sender["balance"]:
            return f"Insufficient balance. Current balance: ₱{sender['balance']:,.2f}"

# ──────────────────// Perform transfer and log transactions
        amount = round(amount, 2)
        sender["balance"]   -= amount
        receiver["balance"] += amount

# ──────────────────// Log transfer transactions for both accounts
        self._log_transaction(from_account,      "Transfer Out", amount,
                              note=f"Transferred ₱{amount:,.2f} to {to_account_number}")
        self._log_transaction(to_account_number, "Transfer In",  amount,
                              note=f"Received ₱{amount:,.2f} from {from_account}")
        return f"Transfer successful. New balance: ₱{sender['balance']:,.2f}"