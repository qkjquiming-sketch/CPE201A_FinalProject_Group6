from file_handlers import JSONFileReaderWriter
from account_manager  import AccountManager
from deposit          import Deposit
from withdrawal       import Withdrawal
from transfer         import Transfer
from statements       import Statements
from change_pin       import ChangePin
from change_password  import ChangePassword
from profile_manager  import ProfileManager

# ──────────────────// Combines all the modules
class Bank(
    AccountManager,
    Deposit,
    Withdrawal,
    Transfer,
    Statements,
    ChangePin,
    ChangePassword,
    ProfileManager
):
    def __init__(self):
        storage = JSONFileReaderWriter()
        super().__init__(storage)