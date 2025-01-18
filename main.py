import sys
import os
import json
sys.stdout.reconfigure(encoding='utf-8')

from models import User  # Импортируем User из models.py

class FinanceManager:
    def __init__(self):
        self.users = {}  # Словарь для хранения пользователей
        self.current_user = None  # Текущий авторизованный пользователь

    def register(self, username, password):
        """Регистрация нового пользователя."""
        if username in self.users:
            raise ValueError("Пользователь уже существует.")
        self.users[username] = User(username, password)  # Создание нового пользователя
        print(f"Пользователь {username} успешно зарегистрирован.")

    def login(self, username, password):
        """Авторизация пользователя."""
        if username not in self.users or self.users[username].password != password:
            raise ValueError("Неверное имя пользователя или пароль.")
        self.current_user = self.users[username]
        self.current_user.wallet.load()  # Загружаем кошелек после входа
        print(f"Пользователь {username} успешно вошёл в систему.")

    def logout(self):
        """Выход из системы."""
        if self.current_user:
            self.current_user.wallet.save()  # Сохраняем кошелек перед выходом
            self.current_user = None
            print("Вы успешно вышли из системы.")

    def process_command(self, command):
        """Обработка команд для работы с кошельком пользователя."""
        if self.current_user is None:
            raise ValueError("Сначала войдите в систему.")
        wallet = self.current_user.wallet

        if command[0] == "add_income":
            wallet.add_income(command[1], float(command[2]))
        elif command[0] == "add_expense":
            wallet.add_expense(command[1], float(command[2]))
        elif command[0] == "set_budget":
            wallet.set_budget(command[1], float(command[2]))
        elif command[0] == "summary":
            summary = wallet.get_summary()
            for key, value in summary.items():
                print(f"{key}: {value}")
        elif command[0] == "export_summary":
            wallet.export_summary(command[1])
            print(f"Сводка успешно сохранена в файл {command[1]}.")
        elif command[0] == "transfer":
            # Команда transfer: transfer <username> <amount>
            if len(command) != 3:
                raise ValueError("Команда 'transfer' требует два аргумента: логин получателя и сумма перевода.")
            
            recipient_username = command[1]
            amount = float(command[2])
            
            if recipient_username not in self.users:
                raise ValueError(f"Пользователь {recipient_username} не найден.")
            
            # Фиксируем расход у отправителя и доход у получателя
            recipient_wallet = self.users[recipient_username].wallet
            
            # Проверка на достаточность средств
            if amount <= 0:
                raise ValueError("Сумма перевода должна быть больше нуля.")
            
            if amount > wallet.balance:
                raise ValueError("Недостаточно средств на балансе для перевода.")
            
            # Выполняем перевод
            wallet.add_expense("Перевод на кошелек " + recipient_username, amount)  # Уменьшаем баланс отправителя
            recipient_wallet.add_income("Перевод от " + self.current_user.username, amount)  # Увеличиваем баланс получателя
            print(f"Перевод {amount} от {self.current_user.username} на {recipient_username} успешно выполнен.")

        else:
            raise ValueError("Неизвестная команда.")


if __name__ == "__main__":
    manager = FinanceManager()

    while True:
        try:
            command = input("Введите команду: ").split()

            if not command:
                continue

            if command[0] == "register":
                if len(command) != 3:
                    raise ValueError("Команда 'register' требует два аргумента: имя пользователя и пароль.")
                manager.register(command[1], command[2])

            elif command[0] == "login":
                if len(command) != 3:
                    raise ValueError("Команда 'login' требует два аргумента: имя пользователя и пароль.")
                manager.login(command[1], command[2])

            elif command[0] == "logout":
                manager.logout()

            elif command[0] == "exit":
                manager.logout()
                print("Приложение завершено.")
                break

            else:
                manager.process_command(command)

        except Exception as e:
            print(f"Ошибка: {e}")
