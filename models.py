import json
import os

class Wallet:
    def __init__(self, username):
        """Конструктор для инициализации кошелька."""
        self.username = username
        self.balance = 0.0  
        self.transactions = []  
        self.budgets = {}  

    def add_income(self, category, amount):
        """Добавить доход."""
        if amount <= 0:
            raise ValueError("Сумма дохода должна быть больше нуля.")
        self.transactions.append({"type": "income", "category": category, "amount": amount})
        self.balance += amount
        print(f"Добавлен доход {amount} на категорию {category}. Баланс: {self.balance}")

    def add_expense(self, category, amount):
        """Добавить расход."""
        if amount <= 0:
            raise ValueError("Сумма расхода должна быть больше нуля.")
        if amount > self.balance:
            raise ValueError("Недостаточно средств для расхода.")
        self.transactions.append({"type": "expense", "category": category, "amount": amount})
        self.balance -= amount
        print(f"Добавлен расход {amount} на категорию {category}. Баланс: {self.balance}")

    def set_budget(self, category, amount):
        """Установить бюджет для категории."""
        if amount <= 0:
            raise ValueError("Бюджет должен быть больше нуля.")
        self.budgets[category] = amount
        print(f"Бюджет для категории {category} установлен на {amount}.")

    def get_summary(self):
        """Получить сводку по кошельку."""
        expenses_by_category = {}
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                category = transaction["category"]
                expenses_by_category[category] = expenses_by_category.get(category, 0) + transaction["amount"]

        summary = {
            "Баланс": self.balance,
            "Доходы": sum(t["amount"] for t in self.transactions if t["type"] == "income"),
            "Расходы": sum(t["amount"] for t in self.transactions if t["type"] == "expense"),
            "Бюджеты": {}
        }

        for category, budget in self.budgets.items():
            spent = expenses_by_category.get(category, 0)
            summary["Бюджеты"][category] = {
                "Бюджет": budget,
                "Потрачено": spent,
                "Остаток": budget - spent
            }

        return summary

    def save(self):
        """Сохранить данные кошелька в файл."""
        if not self.username:
            raise ValueError("Не установлен username для сохранения данных.")
        data = {
            "balance": self.balance,
            "transactions": self.transactions,
            "budgets": self.budgets
        }
        os.makedirs("data", exist_ok=True)
        with open(f"data/{self.username}_wallet.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Данные кошелька сохранены.")

    def load(self):
        """Загрузить данные кошелька из файла."""
        try:
            with open(f"data/{self.username}_wallet.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.balance = data["balance"]
                self.transactions = data["transactions"]
                self.budgets = data["budgets"]
            print("Данные кошелька успешно загружены.")
        except FileNotFoundError:
            print("Файл кошелька не найден, создается новый кошелек.")

class User:
    def __init__(self, username, password):
        """Конструктор для инициализации пользователя."""
        self.username = username
        self.password = password
        self.wallet = Wallet(username)

    def __str__(self):
        """Метод для представления пользователя."""
        return f"User(username={self.username}, password={self.password})"
