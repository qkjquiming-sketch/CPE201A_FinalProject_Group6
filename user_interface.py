import re
import sys
import os
from bank import Bank

# ──────────────────// Clear Screen
def clear():
    os.system('cls' if sys.platform == 'win32' else 'clear')

# ──────────────────// Masked Input (shows * per keypress)
def masked_input(prompt=""):
    print(prompt, end='', flush=True)
    password = ""

    if sys.platform == "win32":
        import msvcrt
        while True:
            ch = msvcrt.getwch()
            if ch in ('\r', '\n'):
                print()
                break
            elif ch == '\x08':
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            elif ch == '\x03':
                raise KeyboardInterrupt
            else:
                password += ch
                print('*', end='', flush=True)
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\r', '\n'):
                    print()
                    break
                elif ch == '\x7f':
                    if password:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                elif ch == '\x03':
                    raise KeyboardInterrupt
                else:
                    password += ch
                    print('*', end='', flush=True) 
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password

# ──────────────────// Dividers
DIV  = "─" * 42
DIV2 = "═" * 42

def header(title):
    print(f"\n{DIV2}")
    print(f"  {title}")
    print(f"{DIV2}\n")

def footer():
    print(f"\n{DIV}\n")

# ──────────────────// User Interface
class UserInterface:
    def __init__(self):
        self.bank    = Bank()
        self.session = None 

# ──────────────────// Name Input
    def _get_name(self):
        while True:
            name = input("Full Name        : ").strip()
            if len(name) >= 2:
                return name
            print("  [!] Name must be at least 2 characters.\n")

# ─────────────────// Account Type Input
    def _get_account_type(self):
        types = ["savings", "checking"]
        while True:
            print("Account Type:")
            for i, t in enumerate(types, 1):
                print(f"  [{i}] {t.capitalize()}")
            choice = input("Choose [1-2]     : ").strip()
            if choice in ("1", "2"):
                return types[int(choice) - 1]
            print("  [!] Please enter 1 or 2.\n")

# ──────────────────// Email Input
    def _get_email(self):
        while True:
            email = input("Email Address    : ").strip()
            if "@" in email and "." in email.split("@")[-1]:
                return email
            print("  [!] Invalid email format.\n")

# ──────────────────// Password Input
    def _get_password(self):
        while True:
            password = masked_input("Password         : ")
            if len(password) < 8:
                print("  [!] Password must be at least 8 characters.\n")
                continue
            confirm = masked_input("Confirm Password : ")
            if password != confirm:
                print("  [!] Passwords do not match.\n")
                continue
            return password

# ──────────────────// PIN Code Input
    def _get_pin_code(self):
        while True:
            pin = masked_input("PIN Code         : ")
            if not pin.isdigit() or len(pin) != 6:
                print("  [!] PIN must be exactly 6 digits.\n")
                continue
            confirm = masked_input("Confirm PIN      : ")
            if pin != confirm:
                print("  [!] PIN codes do not match.\n")
                continue
            return pin

#──────────────────// Amount Input
    def _get_amount(self, label="Amount"):
        while True:
            raw = input(f"{label:<17}: ₱").strip()
            try:
                amount = float(raw)
                if amount <= 0:
                    raise ValueError
                return round(amount, 2)
            except ValueError:
                print("  [!] Enter a valid positive amount.\n")

#──────────────────// Account Number Input
    def _get_account_number_input(self, label="Account Number"):
            while True:
                num = input(f"{label:<17}: ").strip()
                if num == "0":
                    return "0"
                if re.fullmatch(r"\d{12}", num):
                    return num
                print("  [!] Account number must be exactly 12 digits.\n")

#──────────────────// Refresh Session Data
    def _refresh_session(self):
        """Re-reads account from memory so balance/info stays current."""
        self.session = self.bank._get_account(self.session["account_number"])

# ──────────────────// Main Menu
    def main_menu(self):
        while True:
            clear()

            header("BANKING SYSTEM")
            print("  [1] Create Account")
            print("  [2] Login")
            print("  [0] Exit")
            footer()
            choice = input("Select option    : ").strip()

            if   choice == "1": self.create_account_flow()
            elif choice == "2": self.login_flow()
            elif choice == "0":
                print("\n  Goodbye!\n")
                break
            else:
                print("\n  [!] Invalid option.\n")

# ──────────────────// Dashboard and Flows
    def dashboard(self):
        while True:
            self._refresh_session()
            clear()
            acc = self.session
            header(f"DASHBOARD  —  {acc['name']}")
            print(f"  Account No  : {self.bank.format_account_number(acc['account_number'])}")
            print(f"  Type        : {acc['type'].capitalize()}")
            print(f"  Balance     : ₱{acc['balance']:,.2f}")
            print(f"\n{DIV}")
            print("  [1] Deposit")
            print("  [2] Withdraw")
            print("  [3] Transfer Funds")
            print("  [4] Statement History")
            print("  [5] Settings")
            print("  [0] Logout")
            footer()
            choice = input("Select option    : ").strip()

            if   choice == "1": self.deposit_flow()
            elif choice == "2": self.withdraw_flow()
            elif choice == "3": self.transfer_flow()
            elif choice == "4": self.statement_flow()
            elif choice == "5": self.settings_menu()
            elif choice == "0":
                self.session = None
                print("\n  Logged out successfully.\n")
                break
            else:
                print("\n  [!] Invalid option.\n")

# ──────────────────// Settings Menu
    def settings_menu(self):
        while True:
            clear()
            header("SETTINGS")
            print("  [1] Change PIN")
            print("  [2] Change Password")
            print("  [3] Update Profile")
            print("  [0] Back")
            footer()
            choice = input("Select option    : ").strip()

            if   choice == "1": self.change_pin_flow()
            elif choice == "2": self.change_password_flow()
            elif choice == "3": self.update_profile_flow()
            elif choice == "0": break
            else: print("\n  [!] Invalid option.\n")

# ──────────────────// Create Account Flow
    def create_account_flow(self):
        clear()
        header("CREATE NEW ACCOUNT")
        name         = self._get_name()
        account_type = self._get_account_type()
        email        = self._get_email()
        password     = self._get_password()
        pin_code     = self._get_pin_code()
 
        print("\n  Creating account...")
        result = self.bank.create_account(
            name=name, account_type=account_type, email=email,
            password=password, pin_code=pin_code
        )
        print(f"\n  {result}")
        footer()

# ──────────────────// Login Flow
    def login_flow(self):
        clear()
        header("LOGIN")
        print("  [0] Back to Main Menu\n")

        account_number = self._get_account_number_input()
        if account_number == "0":
            return

        while True:
            password = masked_input("Password         : ")
            if password == "0":
                return

            acc, msg = self.bank.login(account_number, password)
            if acc:
                self.session = acc
                print(f"\n  {msg}")
                footer()
                self.dashboard()
                return
            else:
                print(f"\n  [!] {msg}\n")
                if "locked" in msg.lower():
                    footer()
                    return
    
# ──────────────────// Deposit Flow
    def deposit_flow(self):
        clear()
        header("DEPOSIT")
        amount = self._get_amount("Deposit Amount")
        result = self.bank.deposit(self.session["account_number"], amount)
        self._refresh_session()
        print(f"\n  {result}")
        footer()

# ──────────────────// Withdraw Flow
    def withdraw_flow(self):
        clear()
        header("WITHDRAWAL")
        amount = self._get_amount("Withdraw Amount")
        result = self.bank.withdraw(self.session["account_number"], amount)
        self._refresh_session()
        print(f"\n  {result}")
        footer()

# ──────────────────// Transfer Flow
    def transfer_flow(self):
        clear()
        header("TRANSFER FUNDS")
        to_account = self._get_account_number_input("Recipient Acct No")
        amount     = self._get_amount("Transfer Amount")
 
        print(f"\n  Sending ₱{amount:,.2f} → {self.bank.format_account_number(to_account)}")
        confirm = input("  Confirm? [y/n]   : ").strip().lower()
        if confirm != "y":
            print("\n  Transfer cancelled.")
            footer()
            return
 
        result = self.bank.transfer(self.session["account_number"], to_account, amount)
        self._refresh_session()
        print(f"\n  {result}")
        footer()

# ──────────────────// Statement History Flow
    def statement_flow(self):
        clear()
        header("STATEMENT HISTORY")
        statements, err = self.bank.get_statements(self.session["account_number"])
        if err:
            print(f"  [!] {err}")
            footer()
            return
        if not statements:
            print("  No transactions found.")
            footer()
            return
 
        print(f"  {'Date & Time':<22} {'Type':<14} {'Amount':>12}  {'Balance':>12}")
        print(f"  {DIV}")
        for tx in reversed(statements):
            print(f"  {tx['timestamp']:<22} {tx['type']:<14} "
                  f"₱{tx['amount']:>10,.2f}  ₱{tx['balance']:>10,.2f}")
        footer()

# ──────────────────// Change PIN Flow
    def change_pin_flow(self):
        clear()
        header("CHANGE PIN")
        old_pin = masked_input("Current PIN      : ")
        new_pin = self._get_pin_code()
        result  = self.bank.change_pin(self.session["account_number"], old_pin, new_pin)
        print(f"\n  {result}")
        footer()

# ──────────────────// Change Password Flow
    def change_password_flow(self):
        clear()
        header("CHANGE PASSWORD")
        old_pw = masked_input("Current Password : ")
        new_pw = self._get_password()
        result = self.bank.change_password(self.session["account_number"], old_pw, new_pw)
        print(f"\n  {result}")
        footer()

#  ──────────────────// Update Profile Flow
    def update_profile_flow(self):
        clear()
        header("UPDATE PROFILE")
        acc = self.session
        print("  Press Enter to keep current value.\n")
 
        name  = input(f"Full Name        [{acc['name']}]: ").strip() or None
        email = input(f"Email            [{acc['email']}]: ").strip() or None
        phone = input(f"Phone Number     [{acc.get('phone', 'not set')}]: ").strip() or None
 
        result = self.bank.update_profile(
            acc["account_number"], name=name, email=email, phone=phone
        )
        if "successfully" in result:
            self._refresh_session()
        print(f"\n  {result}")
        footer()
