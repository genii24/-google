from telebot import types

MANAGER_ID = 7016453953  # ID менеджера
user_manager_mapping = {}  # Словарь для хранения связи менеджера и пользователя


def register_create_bots_handler(bot):
    """Обработчик для кнопки 'Создание ботов'."""

    @bot.message_handler(func=lambda message: message.text == "🤖 Создание ботов")
    def handle_bots_creation(message):
        """Отправляем главное сообщение с выбором ботов."""
        bot.send_message(
            message.chat.id,
            "🤖 *Создание ботов:*\n\n"
            "Мы предлагаем разработку ботов для Telegram!\n\n"
            "*🎯 Возможности ботов:*\n"
            "- Автоматизация задач.\n"
            "- Рассылка уведомлений.\n"
            "- Сбор данных.\n"
            "- Игры и развлечения.\n"
            "- Подключение к API.\n"
            "- Обработка запросов.\n\n"
            "📩 Свяжитесь с нашим менеджером: @manager\n\n"
            "*👇 Выберите нужный тип бота ниже:*",
            parse_mode="Markdown",
            reply_markup=create_main_inline_keyboard()
        )

    def create_main_inline_keyboard():
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text="🔄 Автоматизация задач", callback_data="bot_task_automation"),
            types.InlineKeyboardButton(text="🔔 Рассылка уведомлений", callback_data="bot_notification"),
            types.InlineKeyboardButton(text="📊 Сбор данных", callback_data="bot_data_collection"),
            types.InlineKeyboardButton(text="🎮 Игры и развлечения", callback_data="bot_games"),
            types.InlineKeyboardButton(text="🔗 Работа с API", callback_data="bot_api_integration"),
            types.InlineKeyboardButton(text="❓ Чат для вопросов", callback_data="bot_qna")
        ]
        keyboard.add(*buttons)
        return keyboard

    def create_back_and_order_keyboard():
        """Создаём inline-кнопки: Назад и Заказать услугу."""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(text="⬅ Назад", callback_data="bot_back"),
            types.InlineKeyboardButton(text="💼 Заказать услугу", callback_data="order_service")
        )
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data.startswith("bot_") or call.data == "order_service")
    def handle_inline_bot_options(call):
        """Обработка выбора опций и кнопки 'Заказать услугу'."""
        if call.data == "bot_task_automation":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="🔄 *Автоматизация задач*\n\n"
                     "Бот поможет:\n"
                     "✅ Автоматически отправлять уведомления.\n"
                     "✅ Управлять бронированием.\n"
                     "✅ Настраивать управление задачами.\n\n"
                     ,
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_notification":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="🔔 *Рассылка уведомлений*\n\n"
                     "Эти боты помогают:\n"
                     "• Уведомлять клиентов в нужное время.\n"
                     "• Настраивать массовую рассылку.\n"
                     "• Работать по расписанию с аудиторией.\n\n"
                     ,
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_data_collection":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="📊 *Сбор данных*\n\n"
                     "Позволяет:\n"
                     "📝 Собирать информацию от пользователей (анкеты, формы).\n"
                     "📊 Интеграция с CRM для анализа.\n"
                     "📂 Хранение и обработка данных.\n",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_games":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="🎮 *Игры и развлечения*\n\n"
                     "Создаём игровые боты:\n"
                     "• Викторины и тесты.\n"
                     "• Игры в режиме реального времени.\n"
                     "• Развлекательные бот-квесты.\n",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_api_integration":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="🔗 *Работа с API*\n\n"
                     "Функционал подключения API:\n"
                     "• CRM-системы, отслеживание заказов.\n"
                     "• Синхронизация с базами данных.\n"
                     "• Автоматизация бизнес-процессов.\n",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_qna":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="❓ *Чат для вопросов*\n\n"
                     "Функции бота для общения:\n"
                     "📨 Отвечает на популярные запросы.\n"
                     "👔 Может перевести сложный вопрос оператору.\n"
                     "📈 Анализирует статистику запросов.\n",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "bot_back":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="⬅ *Главное меню создания ботов:*\n\n"
                     "Выберите нужный тип бота ниже:",
                parse_mode="Markdown",
                reply_markup=create_main_inline_keyboard()
            )
        elif call.data == "order_service":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="📝 *Напишите, пожалуйста, ТЗ (техническое задание), и оно будет отправлено менеджеру.*\n\n"
                     "Ваши ответы можно начинать прямо сейчас.",
                parse_mode="Markdown"
            )

            # Переключаемся в режим "ожидания ответа от пользователя"
            bot.register_next_step_handler_by_chat_id(
                call.message.chat.id, handle_user_tz_submission
            )

    def handle_user_tz_submission(message):
        """Обработка сообщения пользователя с ТЗ."""
        user_tz = message.text
        user_manager_mapping[MANAGER_ID] = message.chat.id  # Привязываем пользователя к менеджеру
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ *Ваше ТЗ успешно отправлено менеджеру!*\n"
                 "Ожидайте, он скоро свяжется с вами.",
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
                text=f"📩 *Ответ от менеджера:*\n{message.text}",
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