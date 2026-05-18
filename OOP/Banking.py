class Account:
    def __init__(self, number, balance, owner):
        self.number = number
        self.balance = balance
        self.owner = owner
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: ${amount}\nNew balance: ${self.balance}\n")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient Funds.\nTotal balance: ${self.balance}\n")

        else:
            self.balance -= amount
            print(f"Withdrew: ${amount}\nNew Balance: ${self.balance}\n")

# --- ACCOUNTS ---
lliw = Account("123", 50, "lliw")
will = Account("6767", 100, "will")
wili = Account("123456", 1000, "wili")

# --- ACCOUNT DICTIONARY ---
accounts = {"123":lliw, "6767":will, "123456":wili}

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

    acc_number = input("\nEnter account number: ")
    if acc_number not in accounts:
        print("Incorrect credentials\n")
    else:
        active = accounts[acc_number]
        print(f"\nWelcome, {active.owner}! [{acc_number}]\nBalance: ${active.balance}\n")

        # --- CHOICES ---
        choice = input("Withdraw [a], Deposit [b], Exit [c]\n").lower()
        if choice == "a":
            w_amount = float(input("\nHow much to withdraw?  $"))
            if w_amount <= 0:
                print("Amount must be positive.")
            else:
                active.withdraw(w_amount)
            
        elif choice == "b":
            d_amount = float(input("\nHow much to deposit?  $"))
            if d_amount <= 0:
                print("Amount must be positive.\n")
            else:
                active.deposit(d_amount)
        elif choice == "c":
            print("\nEnding program...\n")
            exit()
        else:
            print("Invalid")
