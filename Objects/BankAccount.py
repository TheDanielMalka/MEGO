class Bank:
    def __init__(self,name,status,amount = 0):
        self.name = name
        self.status = status
        self.amount = amount
        self.loan = 20000

    def deposit(self):
        self.status += self.amount

    def withdrawl(self):
        if self.status - self.amount < 0:
            return "You don't have enough money"

        else:
            self.status -= self.amount
        return None

    def balance(self):
        return f"Hi {self.name} your balance is {self.status}"

    def loan_check(self):
        if self.status > 20000:
            if 20000 > self.status > 100000:
                print(f"Based on your balance: {self.status} you can have {100000-self.status} loan")
                print(f"With a fee of 13% {self.status * 0.13}")
                inp = input("Do you wanna take a loan? (Y/N)")
                if inp.lower() == "y":
                    levere = input(int("You can have ..... how much you want"))
                    self.status = (self.status + levere)
                    print(f"Congratulations, {self.name} you have {100000-self.status} loan")
                    print(f"With a fee of 13% {self.status * 0.13}")
                    print(f"Your balance is {self.status}")
            if 100000 > self.status > 200000:
                print(f"Based on your balance: {self.status} you can have {200000-self.status} loan")
                print(f"With a fee of 10% {self.status * 0.10}")
            if 200000 > self.status:
                print(f"Based on your balance: {self.status} you can have 10000000 loan")
                print(f"With a fee of 7% {self.status * 0.13}")


