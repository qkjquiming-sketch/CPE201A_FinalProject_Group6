from bank import Bank

bank = Bank()

# ──────────────────// Test Accounts
test_accounts = [
    {
        "name":         "Juan dela Cruz",
        "account_type": "savings",
        "email":        "juan@email.com",
        "password":     "password123",
        "pin_code":     "123456",
        "balance":      5000.00
    },
    {
        "name":         "Maria Santos",
        "account_type": "checking",
        "email":        "maria@email.com",
        "password":     "password123",
        "pin_code":     "123456",
        "balance":      15000.00
    },
    {
        "name":         "Pedro Reyes",
        "account_type": "savings",
        "email":        "pedro@email.com",
        "password":     "password123",
        "pin_code":     "123456",
        "balance":      0.00
    },
]

for data in test_accounts:
    result = bank.create_account(**data)
    print(result)