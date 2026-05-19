class BaseAccount:
    interest_percentage = 0.025

    def __init__(self, number, balance, owner):
        self.number = number
        self.balance = balance
        self.owner = owner
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: ${amount:,.2f}\nNew balance: ${self.balance:,.2f}\n")

    def withdraw(self, amount):
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
        print(f"\nOld balance: ${self.balance:,.2f}")
        new_balance = self.balance * (1 + interest)** time
        interest_added = new_balance - self.balance
        self.balance = new_balance
        print(f"Interest added: ${interest_added:,.2f}\nNew Balance: ${self.balance:,.2f}\n")


class SavingsAccount(BaseAccount):
    interest_percentage = 0.1
    min_balance = 1000

    def add_interest(self, interest):
        if self.balance < self.min_balance:
            print(f"\n[][][]\nBalance below ${self.min_balance:,.2f} == Applying base rate ({BaseAccount.interest_percentage * 100:.2f}%)\n[][][]\n")
            super().add_interest(interest)
        else:
            print(f"\nApplying savings rate ({self.interest_percentage * 100:.2f}%)")
            super().add_interest(self.interest_percentage)

# --- CONFIG ---


# --- ACCOUNTS ---
lliw = SavingsAccount("123", 10000, "lliw")
will = BaseAccount("6767", 50, "will")
wili = BaseAccount("123456", 1000, "wili")
jayden = SavingsAccount("111", 1000, "jayden")

# --- ACCOUNT DICTIONARY ---
accounts = {"123":lliw, "6767":will, "123456":wili, "111":jayden}

# --- MAINLINE ---
first_run = True

while True:
    if first_run:
        first_run = False
    else:

        start = input("Continue [a], Exit [b]\n")
        if start != "a":
            print("\nEnding program...\n")
            exit()
    try:
        acc_number = input("\nEnter account number: ")
    except ValueError:
        print("Invalid input.\n")
        continue
    if acc_number not in accounts:
        print("Invalid credentials\n")
    else:
        active = accounts[acc_number]
        print(f"\nWelcome, {active.owner}! [{acc_number}]\nBalance: ${active.balance:,.2f}\n")

        # --- CHOICES ---
        choice = input("Withdraw [a], Deposit [b], Add interest [c], Exit [d]\n").lower()
        if choice == "a":
            try:
                w_amount = float(input("\nHow much to withdraw?  $"))
            except ValueError:
                print("Invalid input.\n")
                continue
            if w_amount <= 0:
                print("Amount must be positive.\n")
            else:
                active.withdraw(w_amount)
            
        elif choice == "b":
            try:
                d_amount = float(input("\nHow much to deposit?  $"))
            except ValueError:
                print("Invalid input.\n")
                continue
            if d_amount <= 0:
                print("Amount must be positive.\n")
            else:
                active.deposit(d_amount)

        elif choice == "c":
            active.add_interest(active.interest_percentage)

        elif choice == "d":
            print("\nEnding program...\n")
            exit()

        else:
            print("Invalid\n")
