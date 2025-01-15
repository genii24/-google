
from telebot import types

MANAGER_ID = 7016453953  # ID менеджера
user_manager_mapping = {}  # Словарь для хранения связи менеджера и пользователя


def register_premium_handler(bot):
    """Обработчик для кнопки 'Премиум'."""

    @bot.message_handler(func=lambda message: message.text == "💎 Премиум")
    def handle_premium_services(message):
        """Отправляем основное сообщение с описанием премиум-преимуществ и кнопкой 'Купить Премиум'."""
        bot.send_message(
            chat_id=message.chat.id,
            text=(
                "💎 *Премиум услуги*\n\n"
                "Откройте доступ к удивительным возможностям с нашими премиум-услугами:\n\n"
                "✨ *Эксклюзивные преимущества:*\n"
                "- Индивидуальный подход к каждому клиенту.\n"
                "- Высокий уровень приоритета выполнения задач.\n"
                "- Уникальные функции и персонализированные решения.\n"
                "- Наилучшие условия и поддержка.\n\n"
                "💰 *Станьте премиальным клиентом и наслаждайтесь лучшим качеством и сервисами!*"
            ),
            parse_mode="Markdown",
            reply_markup=create_premium_keyboard()
        )

    def create_premium_keyboard():
        """Создаёт кнопку для заказа премиум-услуг."""
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buy_button = types.InlineKeyboardButton(text="💎 Купить Премиум", callback_data="order_service")
        keyboard.add(buy_button)
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data == "order_service")
    def handle_order_service(call):
        """Обрабатывает запрос на заказ премиум-услуги."""
        bot.send_message(
            chat_id=call.message.chat.id,
            text=(
                "📝 *Напишите, пожалуйста, ваши пожелания или ТЗ (техническое задание), и оно будет отправлено менеджеру.*\n\n"
                "Ваши ответы можно начинать прямо сейчас."
            ),
            parse_mode="Markdown"
        )

        # Ожидаем сообщение от пользователя с ТЗ
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_user_tz_submission)

    def handle_user_tz_submission(message):
        """Обрабатывает сообщение с пожеланиями или ТЗ от пользователя."""
        user_tz = message.text
        user_manager_mapping[MANAGER_ID] = message.chat.id  # Привязываем пользователя к менеджеру
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ *Ваше ТЗ успешно отправлено менеджеру!*\nОжидайте, он скоро свяжется с вами.",
            parse_mode="Markdown"
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="✏️ Ответить", callback_data="reply_to_user"))

        bot.send_message(
            chat_id=MANAGER_ID,
            text=f"📩 *Новое ТЗ от пользователя:*\n"
                 f"👤 Пользователь: @{message.from_user.username or 'Нет ника'}\n"
                 f"💬 Текст ТЗ:\n{user_tz}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "reply_to_user")
    def handle_reply_to_user(call):
        """Менеджер нажимает кнопку 'Ответить', вводит текст ответа."""
        bot.send_message(
            chat_id=call.message.chat.id,
            text="✉️ *Введите текст ответа для пользователя.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, send_reply_to_user)

    def send_reply_to_user(message):
        """Отправка ответа от менеджера пользователю."""
        user_id = user_manager_mapping.get(message.chat.id)
        if user_id:
            bot.send_message(
                chat_id=user_id,
                text=f"📩 *Ответ от менеджера:*\n\n{message.text}",
                parse_mode="Markdown"
            )
            bot.send_message(
                chat_id=message.chat.id,
                text="✅ Ответ успешно отправлен пользователю.",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="❌ Ошибка: Пользователь не найден.",
                parse_mode="Markdown"
            )
