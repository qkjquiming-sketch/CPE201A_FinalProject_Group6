import re
from acc_num_generator import AccountNumberGenerator
from account_store import AccountStore
from file_handlers import JSONFileReaderWriter

# ──────────────────// Account Manager
class AccountManager(AccountStore):
    def __init__(self, storage: JSONFileReaderWriter):
        super().__init__(storage)

# ──────────────────// Account Creation
    def create_account(self, name, account_type, email, password, pin_code, balance=0):
        self.accounts = self._load_accounts() # Reload accounts to get latest data

# ──────────────────// Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email address."

# ──────────────────// Validate pin code format
        if not re.fullmatch(r"\d{6}", str(pin_code)):
            return "Pin code must be exactly 6 digits."

# ──────────────────// Validate password length
        if len(password) < 8:
            return "Password must be at least 8 characters."

# ──────────────────// Check for duplicate email
        for acc in self.accounts.values():
            if acc.get("email") == email:
                return "Email is already in use."

# ──────────────────// Create account
        account_number  = AccountNumberGenerator.generate_unique(self.accounts)
        hashed_password = self._hash(password)
        hashed_pin      = self._hash(pin_code)

        self.accounts[account_number] = {
            "account_number": account_number,
            "name":           name,
            "type":           account_type,
            "email":          email,
            "password":       hashed_password,
            "pin_code":       hashed_pin,
            "balance":        balance,
            "status":         "active",
            "login_attempts": 0
        }
        self._save(account_number)
        formatted = self.format_account_number(account_number)
        return f"Account created successfully. Account Number: {formatted}"

# ──────────────────// Login / Authentication
    def login(self, account_number, password):
        from account_store import MAX_LOGIN_ATTEMPTS
 
        acc = self._get_account(account_number)
        if not acc:
            return None, "Account not found."
 
        if acc.get("status") == "locked":
            return None, "Account is locked due to too many failed login attempts. Contact support."
 
        if acc["password"] != self._hash(password):
            acc["login_attempts"] = acc.get("login_attempts", 0) + 1
            remaining = MAX_LOGIN_ATTEMPTS - acc["login_attempts"]
 
            if acc["login_attempts"] >= MAX_LOGIN_ATTEMPTS:
                acc["status"] = "locked"
                self._save(account_number)
                return None, "Account locked after too many failed attempts."
 
            self._save(account_number)
            return None, f"Incorrect password. {remaining} attempt(s) remaining."
 
        acc["login_attempts"] = 0
        self._save(account_number)
        return acc, "Login successful."