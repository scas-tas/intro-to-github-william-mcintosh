class BaseAccount:
    interest_percentage = 0.025

    def __init__(self, number, balance, owner):
        self.number = number
        self.balance = balance
        self.owner = owner
    
    def deposit(self):
        try:
            amount = float(input("\nHow much to deposit?    $"))
        except ValueError:
            print("Invalid input.\n")
            return
        if amount <= 0:
            print("Amount must be positive.\n")
            return
        self.balance += amount
        print(f"Deposited: ${amount:,.2f}\nNew balance: ${self.balance:,.2f}\n")

    def withdraw(self):
        try:
            amount = float(input("\nHow much to withdraw    $"))
        except ValueError:
            print("Invalid input.\n")
            return
        if amount <= 0:
            print("Amount must be positive.\n")
            return
        if amount > self.balance:
            print(f"Insufficient Funds.\nTotal balance: ${self.balance:,.2f}\n")
        else:
            self.balance -= amount
            print(f"Withdrew: ${amount:,.2f}\nNew Balance: ${self.balance:,.2f}\n")
    
    def add_interest(self, interest):
        time = float(input("\nHow many years: "))
        if time != int(time) or time < 1:
            print("Must be greater than or equal to 1 year\n")
            return
        time = int(time)
        try:
            new_balance = self.balance * (1 + interest)** time
            interest_added = new_balance - self.balance
        except OverflowError:
            print("Invalid input == Number too large.\n")
            return
        old_balance = self.balance
        self.balance = new_balance
        print(f"\nOld balance: ${old_balance:,.2f}")
        print(f"Interest added: ${interest_added:,.2f}")
        print(f"New Balance: ${self.balance:,.2f}\n")

    def welcome(self):
        print(f"\nWelcome, {self.owner}! [{self.number}]")
        print(f"Balance:    ${self.balance:,.2f}\n")

    def handle_choice(self):
        choice = input("Withdraw [a], Deposit [b], Add interest [c], Exit [d]\n").lower()
        if choice == "a":
            self.withdraw()
        elif choice =="b":
            self.deposit()
        elif choice =="c":
            self.add_interest(self.interest_percentage)
        elif choice == "d":
            print("\nEnding program...\n")
            exit()
        else:
            print("Invalid\n")

class SavingsAccount(BaseAccount):
    interest_percentage = 0.1
    min_balance = 1000

    def add_interest(self, interest):
        if self.balance < self.min_balance:
            print(f"\n[!][!][!]\nBalance below ${self.min_balance:,.2f} == Applying base rate ({BaseAccount.interest_percentage * 100:.2f}%)\n[!][!][!]\n")
            super().add_interest(interest)
        else:
            print(f"\nApplying savings rate ({self.interest_percentage * 100:.2f}%)")
            super().add_interest(self.interest_percentage)

class TermAccount(SavingsAccount):
    interest_percentage = 0.15
    min_balance = 1000
    term = 1
    def __init__(self, number, balance, owner):
        super().__init__(number, balance, owner)
        self.locked = True
        self.years_of_interest = 0

    def is_finished(self):
        return not self.locked
    
    def unlock(self):
        self.locked = False
        print("Term has finished. Withdrawals are now avaliable.")

    def welcome(self):
        super().welcome()
        status = "Unlocked" if self.is_finished() else f"Locked ({self.years_of_interest}/{self.term} years)"
        print(f"Term status: {status}\n")

    def withdraw(self):
        if self.locked:
            if self.years_of_interest >= self.term:
                print("Your interest has covered the full term == Lock removed automatically.\n")
                self.unlock()
                super().withdraw()
            else:
                confirm = input(f"Account locked ({self.years_of_interest}/{self.term} years completed). Withdraw anyways [y/n]:").lower()
                if confirm == "y":
                    self.unlock()
                    super().withdraw()
                else:
                    print("Withdrawal cancelled.\n")
        else:
            super().withdraw()

    def add_interest(self, interest):
        time = float(input("\nHow many years: "))
        if time != int(time) or time < 1:
            print("Must be greater than or equal to 1 year.\n")
            return
        time = int(time)
        self.years_of_interest += time
        print(f"\nApplying term savings rate ({self.interest_percentage * 100:.2f}%)")
        super(SavingsAccount, self).add_interest(self.interest_percentage)
        if self.years_of_interest >= self.term and self.locked:
            print(f"Term complete ({self.years_of_interest} year(s) of interest added) == Account unlocked\n")
            self.unlock()

# --- ACCOUNTS ---
lliw = SavingsAccount("123", 10000, "lliw")
will = BaseAccount("6767", 50, "will")
wili = BaseAccount("123456", 1000, "wili")
jayden = SavingsAccount("111", 1000, "jayden")
bob = TermAccount("222", 10000, "bob")

# --- ACCOUNT DICTIONARY ---
accounts = {"123":lliw, "6767":will, "123456":wili, "111":jayden, "222":bob}

# --- FUNCTIONS ---

def get_account():
    acc_number = input("\nEnter account number: ")
    if acc_number not in accounts:
        print("Invalid credentials.\n")
        return None
    return accounts[acc_number]

def cont_prompt():
    start = input("Continue [a], Exit [b]\n")
    if start != "a":
        print("Ending program...")
        exit()

# --- MAINLINE ---

first_run = True

while True:
    if first_run:
        first_run = False
    else:
        cont_prompt()
    
    active = get_account()
    if active is None:
        continue

    active.welcome()
    active.handle_choice()