from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, balance=0.0):
        self._balance = balance  # Private attribute: balance

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @property
    def balance(self):
        return self._balance

class SavingsAccount(BankAccount):
    def __init__(self, balance=0.0):
        super().__init__(balance)

    def deposit(self, amount):
        if amount > 100:
            print("Minimum deposit is $100.")
        else:
            super().deposit(amount)

    def withdraw(self, amount):
        self.deposit(-amount)  # Overriding the inherited method to check for overdraft

# Example usage
if __name__ == "__main__":
    account = BankAccount(500.0)

    print(f"Initial balance: {account.balance}")

    account.deposit(2000.0)
    print(f"After depositing $2000: {account.balance}")

    account.withdraw(1500.0)  # Should print an error message