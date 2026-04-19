import os, hashlib, json
from datetime import datetime
from file_handlers import JSONFileReaderWriter, CSVFileReaderWriter

# ──────────────────// Account Directory
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNT_DIR = os.path.join(BASE_DIR, "Accounts")
STATEMENTS_DIR = os.path.join(BASE_DIR, "Statements")

if not os.path.exists(ACCOUNT_DIR):
    os.makedirs(ACCOUNT_DIR)
if not os.path.exists(STATEMENTS_DIR):
    os.makedirs(STATEMENTS_DIR)

# ──────────────────// Constants
MAX_LOGIN_ATTEMPTS = 5

# ──────────────────// Account Store
class AccountStore:
    def __init__(self, storage: JSONFileReaderWriter):
        self.storage  = storage
        self.csv_storage = CSVFileReaderWriter()
        self.accounts = self._load_accounts()

# ──────────────────// File Path Helper
    def _account_filepath(self, account_number):
        return os.path.join(ACCOUNT_DIR, f"{account_number}.json")

# ──────────────────// Load All Accounts
    def _load_accounts(self):
        """Reads every .json file in ACCOUNT_DIR into memory."""
        accounts = {}
        for filename in os.listdir(ACCOUNT_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(ACCOUNT_DIR, filename)
                try:
                    data    = self.storage.read(filepath)
                    acc_num = data.get("account_number")
                    if acc_num:
                        accounts[acc_num] = data
                except Exception:
                    pass
        return accounts

# ──────────────────// Save Single Account
    def _save(self, account_number):
        """Persists one account to its own JSON file."""
        filepath = self._account_filepath(account_number)
        self.storage.write(filepath, self.accounts[account_number])

# ──────────────────// Hash Helper
    @staticmethod
    def _hash(value):
        return hashlib.sha256(str(value).encode()).hexdigest()

# ──────────────────// Account Number Formatter
    @staticmethod
    def format_account_number(account_number):
        """Formats a 12-digit number as #### #### ####"""
        n = str(account_number)
        return ' '.join(n[i:i+4] for i in range(0, len(n), 4))

# ──────────────────// Account Lookup
    def _get_account(self, account_number):
        """Returns account dict or None."""
        return self.accounts.get(account_number)

# ──────────────────// Statements Filepath
    def _statements_filepath(self, account_number):
        return os.path.join(STATEMENTS_DIR, f"{account_number}_statements.csv")

# ──────────────────// Load Statements
    def _load_statements(self, account_number):
        filepath = self._statements_filepath(account_number)
        if not os.path.exists(filepath):
            return []
        try:
            return self.csv_storage.read_csv(filepath)
        except Exception:
            return []

# ──────────────────// Log Transactions
    def _log_transaction(self, account_number, tx_type, amount, note=""):
        acc = self.accounts[account_number]
        row = {
            "type":      tx_type,
            "amount":    amount,
            "balance":   acc["balance"],
            "note":      note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.csv_storage.append_csv(self._statements_filepath(account_number), row)
        self._save(account_number)