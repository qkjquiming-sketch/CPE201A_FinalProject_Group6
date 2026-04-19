import random

# ──────────────────// Random Account Number Generator //──────────────────
class AccountNumberGenerator:
    @staticmethod
    def generate():
        """Generates a random 12-digit account number (zero-padded)."""
        return str(random.randint(0, 999999999999)).zfill(12)

    @staticmethod
    def generate_unique(existing_accounts: dict):
        """Generates a 12-digit account number not already in existing_accounts."""
        while True:
            number = str(random.randint(0, 999999999999)).zfill(12)
            if number not in existing_accounts:
                return number