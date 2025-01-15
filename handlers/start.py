import os
from telebot import types


def register_start_handler(bot):
    @bot.message_handler(commands=["start"])
    def start_command(message):
        """Обработчик команды /start."""
        user_id = message.chat.id
        user_name = message.from_user.first_name

        # Приветствие
        bot.send_message(
            message.chat.id,
            f"Привет, {user_name}! 👋\nВаш ID: {user_id}"
        )

        if is_user_registered(user_id):
            # Если пользователь зарегистрирован, запросим у него пароль
            bot.send_message(message.chat.id, "Введите ваш пароль:")
            bot.register_next_step_handler(message, verify_password, user_id)
        else:
            # Если пользователя нет в базе, запросим создание нового пароля
            bot.send_message(message.chat.id, "Вы новый пользователь!\nПожалуйста, придумайте пароль для регистрации.")
            bot.register_next_step_handler(message, register_new_password, user_id)

    def register_new_password(message, user_id):
        """Обрабатываем и сохраняем новый пароль пользователя."""
        user_password = message.text.strip()  # Получаем введённый пароль
        save_user_data(user_id, user_password, message.from_user.first_name)
        send_welcome_message(message)

    def verify_password(message, user_id):
        """Проверяем введённый пароль для существующего пользователя."""
        user_password = message.text.strip()
        if check_user_password(user_id, user_password):
            send_welcome_message(message)
        else:
            bot.send_message(message.chat.id, "🚫 Неверный пароль. Попробуйте ещё раз.")
            bot.register_next_step_handler(message, verify_password, user_id)

    def send_welcome_message(message):
        """Отправляет сообщение с приветствием и inline-кнопками."""
        bot_name = "Ваш Надёжный Бот"  # Имя бота
        # Сообщение с приветствием
        bot.send_message(
            message.chat.id,
            f"Приятно познакомиться! Меня зовут {bot_name}. 🤖\n"
            "Я буду вашим надёжным другом в эти суровые времена. 🛡️\n"
            "Давайте начнём работу! 🚀"
        )

        # Создание Inline-кнопок
        keyboard = types.InlineKeyboardMarkup()
        rules_button = types.InlineKeyboardButton("📘 Правила", url="https://example.com/rules")
        main_menu_button = types.InlineKeyboardButton("🏠 Главное меню",
                                                      callback_data="main_menu")  # Связано с main_menu.py
        keyboard.add(rules_button, main_menu_button)

        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

    def is_user_registered(user_id):
        """Проверяет, зарегистрирован ли пользователь в файле users.txt."""
        if not os.path.exists("users.txt"):
            return False

        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                if f"ID {user_id}:" in line:
                    return True
        return False

    def save_user_data(user_id, password, username):
        """Сохраняет данные нового пользователя в файл users.txt."""
        with open("users.txt", "a", encoding="utf-8") as file:
            file.write(f"Пользователь: {username}\n")
            file.write(f"ID {user_id}: {password}\n")
            file.write("-----\n")

    def check_user_password(user_id, password):
        """Проверяет, соответствует ли пароль пользователя введённым данным."""
        if not os.path.exists("users.txt"):
            return False

        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file:
                if f"ID {user_id}:" in line and f": {password}" in line:
                    return True
        return False