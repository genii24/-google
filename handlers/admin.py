from telebot import types

# Список пользователей загружается из файла users.txt
registered_users = []


def load_registered_users():
    """Загрузка списка зарегистрированных пользователей из файла users.txt."""
    global registered_users
    try:
        with open("users.txt", "r", encoding="utf-8") as file:
            for line in file.readlines():
                if "ID" in line:  # Ищем строки с ID
                    user_id = int(line.split("ID")[1].split(":")[0].strip())
                    registered_users.append(user_id)
    except FileNotFoundError:
        print("⚠️ Файл users.txt не найден. Создайте файл с пользователями.")
    except Exception as e:
        print(f"Ошибка загрузки пользователей: {e}")


def save_registered_users():
    """Сохранение списка зарегистрированных пользователей в файл users.txt."""
    try:
        with open("users.txt", "w", encoding="utf-8") as file:
            for user_id in registered_users:
                file.write(f"ID {user_id}:\n")
    except Exception as e:
        print(f"Ошибка сохранения пользователей: {e}")


def register_admin_handler(bot):
    """Хендлеры для админ-панели."""

    load_registered_users()  # Загружаем пользователей при запуске

    @bot.message_handler(func=lambda message: message.text == "/admin" and message.chat.id == 7016453953)
    def admin_panel(message):
        """Главное меню админ-панели."""
        bot.send_message(
            message.chat.id,
            "🔧 *Админ-панель:*\nВыберите действие:",
            reply_markup=admin_main_menu(),
            parse_mode="Markdown"
        )

    def admin_main_menu():
        """Главное меню админ-панели - клавиатура."""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton(text="📢 Отправить объявление", callback_data="admin_broadcast"),
            types.InlineKeyboardButton(text="📋 Просмотреть запросы", callback_data="admin_view_requests"),
            types.InlineKeyboardButton(text="⭐ Отправить сообщение пользователю", callback_data="admin_direct_message"),
            types.InlineKeyboardButton(text="➕ Добавить пользователя", callback_data="admin_add_user"),
            types.InlineKeyboardButton(text="❌ Удалить пользователя", callback_data="admin_remove_user"),
        ]
        keyboard.add(*buttons)
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data == "admin_direct_message")
    def admin_direct_message(call):
        """Админ - отправка сообщения конкретному пользователю."""
        bot.send_message(
            call.message.chat.id,
            "✏️ *Введите ID пользователя, которому хотите отправить сообщение.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_direct_message_id)

    def handle_direct_message_id(message):
        """Получение ID пользователя для отправки сообщения."""
        try:
            user_id = int(message.text)
            if user_id in registered_users:
                bot.send_message(
                    message.chat.id,
                    f"✅ Пользователь с ID {user_id} найден. Теперь введите текст сообщения.",
                    parse_mode="Markdown"
                )
                bot.register_next_step_handler_by_chat_id(message.chat.id, handle_direct_message_text, user_id)
            else:
                bot.send_message(
                    message.chat.id,
                    "⚠️ Пользователь с данным ID не зарегистрирован.",
                    parse_mode="Markdown"
                )
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ Неверный формат ID пользователя. Попробуйте ещё раз.",
                parse_mode="Markdown"
            )

    def handle_direct_message_text(message, user_id):
        """Получение текста сообщения и отправка пользователю."""
        text = message.text
        try:
            bot.send_message(user_id, f"📩 *Сообщение от администратора:*\n{text}", parse_mode="Markdown")
            bot.send_message(
                message.chat.id,
                f"✅ Сообщение успешно отправлено пользователю с ID {user_id}.",
                parse_mode="Markdown"
            )
        except Exception as e:
            bot.send_message(
                message.chat.id,
                f"❌ Не удалось отправить сообщение пользователю с ID {user_id}. Ошибка: {e}",
                parse_mode="Markdown"
            )

    @bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
    def admin_broadcast(call):
        """Админ - отправка объявлений."""
        bot.send_message(
            call.message.chat.id,
            "✏️ *Введите текст объявления, которое хотите разослать всем пользователям.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_broadcast_message)

    def handle_broadcast_message(message):
        """Обработка текста для массовой рассылки."""
        announcement = message.text

        if not registered_users:
            bot.send_message(
                message.chat.id,
                "⚠️ Пользователи для рассылки не зарегистрированы.",
                parse_mode="Markdown"
            )
            return

        for user_id in registered_users:
            try:
                bot.send_message(
                    user_id,
                    f"📢 *Новое объявление:*\n{announcement}",
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

        bot.send_message(
            message.chat.id,
            "✅ Объявление успешно отправлено пользователям!",
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "admin_add_user")
    def admin_add_user(call):
        """Админ - добавление пользователя."""
        bot.send_message(
            call.message.chat.id,
            "✏️ *Введите ID пользователя, которого хотите добавить.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_add_user)

    def handle_add_user(message):
        """Обработка добавления пользователя."""
        try:
            user_id = int(message.text)
            if user_id not in registered_users:
                registered_users.append(user_id)
                save_registered_users()  # Сохраняем в файл
                bot.send_message(
                    message.chat.id,
                    f"✅ Пользователь с ID {user_id} успешно добавлен.",
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"⚠️ Пользователь с ID {user_id} уже зарегистрирован.",
                    parse_mode="Markdown"
                )
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ Неверный формат ID пользователя. Попробуйте ещё раз.",
                parse_mode="Markdown"
            )

    @bot.callback_query_handler(func=lambda call: call.data == "admin_remove_user")
    def admin_remove_user(call):
        """Админ - удаление пользователя."""
        bot.send_message(
            call.message.chat.id,
            "✏️ *Введите ID пользователя, которого хотите удалить.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_remove_user)

    def handle_remove_user(message):
        """Обработка удаления пользователя."""
        try:
            user_id = int(message.text)
            if user_id in registered_users:
                registered_users.remove(user_id)
                save_registered_users()  # Сохраняем изменения в файл
                bot.send_message(
                    message.chat.id,
                    f"✅ Пользователь с ID {user_id} успешно удалён.",
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(
                    message.chat.id,
                    f"⚠️ Пользователя с ID {user_id} нет в списке.",
                    parse_mode="Markdown"
                )
        except ValueError:
            bot.send_message(
                message.chat.id,
                "❌ Неверный формат ID пользователя. Попробуйте ещё раз.",
                parse_mode="Markdown"
            )