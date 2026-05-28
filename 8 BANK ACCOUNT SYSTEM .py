# banking_system.py
import json
import random
from datetime import datetime

class Account:
    """Base class for all accounts"""
    def __init__(self, account_number, holder_name, initial_deposit=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = initial_deposit
        self.transactions = []
        self.created_date = datetime.now()
        self.add_transaction("Account opened", initial_deposit)
    
    def add_transaction(self, description, amount):
        """Record a transaction"""
        self.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "description": description,
            "amount": amount,
            "balance": self.balance
        })
    
    def deposit(self, amount):
        """Deposit money"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        
        self.balance += amount
        self.add_transaction("Deposit", amount)
        return True
    
    def withdraw(self, amount):
        """Withdraw money"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds!")
        
        self.balance -= amount
        self.add_transaction("Withdrawal", -amount)
        return True
    
    def get_balance(self):
        """Get current balance"""
        return self.balance
    
    def get_transactions(self, limit=10):
        """Get last n transactions"""
        return self.transactions[-limit:]
    
    def to_dict(self):
        """Convert account to dictionary"""
        return {
            "type": self.__class__.__name__,
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "balance": self.balance,
            "transactions": self.transactions,
            "created_date": self.created_date.isoformat()
        }

class SavingsAccount(Account):
    """Savings account with interest"""
    def __init__(self, account_number, holder_name, initial_deposit=0, interest_rate=0.02):
        super().__init__(account_number, holder_name, initial_deposit)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        """Add interest to account"""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.add_transaction(f"Interest earned ({self.interest_rate*100}%)", interest)
        return interest
    
    def to_dict(self):
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data

class CheckingAccount(Account):
    """Checking account with overdraft protection"""
    def __init__(self, account_number, holder_name, initial_deposit=0, overdraft_limit=500):
        super().__init__(account_number, holder_name, initial_deposit)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        """Withdraw with overdraft protection"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive!")
        
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Exceeds overdraft limit!")
        
        self.balance -= amount
        self.add_transaction("Withdrawal", -amount)
        
        if self.balance < 0:
            overdraft_fee = 35
            self.balance -= overdraft_fee
            self.add_transaction("Overdraft fee", -overdraft_fee)
        
        return True
    
    def to_dict(self):
        data = super().to_dict()
        data["overdraft_limit"] = self.overdraft_limit
        return data

class Bank:
    def __init__(self):
        self.accounts = {}
        self.filename = "bank_data.json"
        self.load_data()
    
    def generate_account_number(self):
        """Generate unique account number"""
        while True:
            number = str(random.randint(10000, 99999))
            if number not in self.accounts:
                return number
    
    def create_account(self):
        """Create a new bank account"""
        print("\n🏦 Create New Account")
        print("Account Types:")
        print("1. Savings Account (earns interest)")
        print("2. Checking Account (overdraft allowed)")
        
        try:
            acc_type = input("Choose type (1-2): ")
            
            name = input("Account holder name: ").strip()
            if not name:
                print("❌ Name is required!")
                return
            
            try:
                initial = float(input("Initial deposit ($): "))
                if initial < 0:
                    print("❌ Initial deposit cannot be negative!")
                    return
            except ValueError:
                print("❌ Invalid amount!")
                return
            
            account_number = self.generate_account_number()
            
            if acc_type == "1":
                account = SavingsAccount(account_number, name, initial)
            elif acc_type == "2":
                account = CheckingAccount(account_number, name, initial)
            else:
                print("❌ Invalid account type!")
                return
            
            self.accounts[account_number] = account
            self.save_data()
            
            print(f"\n✅ Account created successfully!")
            print(f"📋 Account Number: {account_number}")
            print(f"👤 Holder: {name}")
            print(f"💰 Initial Balance: ${initial:.2f}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def find_account(self):
        """Find account by number"""
        acc_num = input("Enter account number: ").strip()
        
        if acc_num in self.accounts:
            return self.accounts[acc_num]
        else:
            print("❌ Account not found!")
            return None
    
    def deposit_money(self):
        """Deposit money to account"""
        account = self.find_account()
        if not account:
            return
        
        try:
            amount = float(input("Amount to deposit: $"))
            account.deposit(amount)
            self.save_data()
            print(f"✅ Deposited ${amount:.2f}")
            print(f"💰 New balance: ${account.get_balance():.2f}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def withdraw_money(self):
        """Withdraw money from account"""
        account = self.find_account()
        if not account:
            return
        
        try:
            amount = float(input("Amount to withdraw: $"))
            account.withdraw(amount)
            self.save_data()
            print(f"✅ Withdrew ${amount:.2f}")
            print(f"💰 New balance: ${account.get_balance():.2f}")
        except ValueError as e:
            print(f"❌ Error: {e}")
    
    def check_balance(self):
        """Check account balance"""
        account = self.find_account()
        if not account:
            return
        
        print(f"\n📊 ACCOUNT STATEMENT")
        print("="*40)
        print(f"Account: {account.account_number}")
        print(f"Holder: {account.holder_name}")
        print(f"Type: {account.__class__.__name__}")
        print(f"Balance: ${account.get_balance():.2f}")
        print("="*40)
    
    def view_transactions(self):
        """View transaction history"""
        account = self.find_account()
        if not account:
            return
        
        transactions = account.get_transactions()
        
        print(f"\n📜 TRANSACTION HISTORY for {account.holder_name}")
        print("="*60)
        print(f"{'Date':<20} {'Description':<20} {'Amount':>10} {'Balance':>10}")
        print("="*60)
        
        for trans in transactions:
            date = trans['date'].split()[0]
            amount = trans['amount']
            amount_str = f"${amount:.2f}" if amount >= 0 else f"-${abs(amount):.2f}"
            print(f"{date:<20} {trans['description']:<20} {amount_str:>10} ${trans['balance']:>9.2f}")
    
    def add_interest(self):
        """Add interest to savings accounts"""
        for account in self.accounts.values():
            if isinstance(account, SavingsAccount):
                interest = account.add_interest()
                print(f"💰 Added ${interest:.2f} interest to account {account.account_number}")
        self.save_data()
    
    def save_data(self):
        """Save all accounts to file"""
        data = {}
        for acc_num, account in self.accounts.items():
            data[acc_num] = account.to_dict()
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load accounts from file"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            for acc_num, acc_data in data.items():
                if acc_data["type"] == "SavingsAccount":
                    account = SavingsAccount(
                        acc_data["account_number"],
                        acc_data["holder_name"],
                        acc_data["balance"],
                        acc_data.get("interest_rate", 0.02)
                    )
                else:  # CheckingAccount
                    account = CheckingAccount(
                        acc_data["account_number"],
                        acc_data["holder_name"],
                        acc_data["balance"],
                        acc_data.get("overdraft_limit", 500)
                    )
                
                account.transactions = acc_data["transactions"]
                account.created_date = datetime.fromisoformat(acc_data["created_date"])
                self.accounts[acc_num] = account
        
        except FileNotFoundError:
            pass

def main():
    bank = Bank()
    
    while True:
        print("\n🏦 BANKING SYSTEM")
        print("="*40)
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. Apply Interest (Savings Accounts)")
        print("7. Exit")
        print("="*40)
        
        choice = input("Choose (1-7): ")
        
        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.deposit_money()
        elif choice == "3":
            bank.withdraw_money()
        elif choice == "4":
            bank.check_balance()
        elif choice == "5":
            bank.view_transactions()
        elif choice == "6":
            bank.add_interest()
        elif choice == "7":
            print("\nThank you for banking with us! 👋")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()