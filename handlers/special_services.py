from telebot import types

MANAGER_ID = 7016453953  # ID менеджера
user_manager_mapping = {}  # Словарь для связи пользователя и менеджера


def register_special_services_handler(bot):
    """Обработчик для кнопки 'Спец. сервисы'."""

    @bot.message_handler(func=lambda message: message.text == "🛠 Спец. сервисы")
    def handle_special_services(message):
        bot.send_message(
            message.chat.id,
            "💳 **Приём заливов на карты стран СНГ:**\n\n"
            "Мы принимаем средства на наши карты из стран СНГ. Выберите страну, чтобы начать:",
            parse_mode="Markdown",
            reply_markup=create_country_keyboard()
        )

    def create_country_keyboard():
        """Создание клавиатуры с кнопками стран СНГ."""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        countries = [
            ("🇷🇺 Россия", "country_russia"),
            ("🇰🇿 Казахстан", "country_kazakhstan"),
            ("🇧🇾 Беларусь", "country_belarus"),
            ("🇺🇿 Узбекистан", "country_uzbekistan"),
            ("🇰🇬 Кыргызстан", "country_kyrgyzstan"),
            ("🇦🇲 Армения", "country_armenia"),
        ]
        buttons = [
            types.InlineKeyboardButton(text=country[0], callback_data=country[1])
            for country in countries
        ]
        keyboard.add(*buttons)
        return keyboard

    def create_transaction_keyboard():
        """Кнопка 'Начать сделку'."""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(text="💼 Начать сделку", callback_data="start_transaction")
        )
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
    def handle_country_selection(call):
        """Обработка выбора страны."""
        country_name_map = {
            "country_russia": "🇷🇺 *Россия*",
            "country_kazakhstan": "🇰🇿 *Казахстан*",
            "country_belarus": "🇧🇾 *Беларусь*",
            "country_uzbekistan": "🇺🇿 *Узбекистан*",
            "country_kyrgyzstan": "🇰🇬 *Кыргызстан*",
            "country_armenia": "🇦🇲 *Армения*",
        }
        country_name = country_name_map.get(call.data, "🏳️ Неизвестная страна")
        bot.send_message(
            call.message.chat.id,
            f"{country_name}\n\n"
            "Вы выбрали страну. Нажмите кнопку ниже, чтобы начать сделку.",
            parse_mode="Markdown",
            reply_markup=create_transaction_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data == "start_transaction")
    def handle_start_transaction(call):
        """Начало сделки — запрос данных для сделки."""
        bot.send_message(
            call.message.chat.id,
            "📝 *Введите данные для сделки:*\n"
            "- На какую карту нужно сделать перевод.\n"
            "- Желаемая сумма.\n\n"
            "После этого запрос будет передан менеджеру.",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_transaction_details)

    def handle_transaction_details(message):
        """Обработка введённых данных для сделки."""
        user_manager_mapping[MANAGER_ID] = message.chat.id  # Привязываем пользователя к менеджеру
        transaction_details = message.text
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ *Ваш запрос отправлен менеджеру!*\n"
                 "Ожидайте дальнейших инструкций.",
            parse_mode="Markdown"
        )
        # Отправка данных менеджеру с кнопками
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_to_user_{message.chat.id}"),
            types.InlineKeyboardButton(text="📋 Заготовленные ответы",
                                       callback_data=f"prepared_replies_{message.chat.id}")
        )

        bot.send_message(
            chat_id=MANAGER_ID,
            text=f"📩 *Новый запрос на сделку:*\n"
                 f"👤 Пользователь: @{message.from_user.username or 'Нет ника'}\n"
                 f"💬 Данные:\n{transaction_details}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_to_user_"))
    def handle_reply_to_user(call):
        """Обработка ответа менеджера пользователю."""
        user_id = int(call.data.split("_")[-1])  # Извлечение ID пользователя из callback_data
        bot.send_message(
            chat_id=call.message.chat.id,
            text="✉️ *Введите текст ответа для пользователя.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, send_reply_to_user, user_id)

    def send_reply_to_user(message, user_id):
        """Отправка ответа менеджера пользователю."""
        bot.send_message(
            chat_id=user_id,
            text=f"📩 *Ответ от менеджера:*\n{message.text}",
            parse_mode="Markdown"
        )
        bot.send_message(
            chat_id=MANAGER_ID,
            text="✅ Сообщение отправлено пользователю.",
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("prepared_replies_"))
    def handle_prepared_replies(call):
        """Обработка заготовленных ответов."""
        user_id = int(call.data.split("_")[-1])  # Извлечение ID пользователя
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        # Заготовленные ответы
        replies = {
            "reply_1": "Мы приняли ваш запрос. Ожидайте обработки.",
            "reply_2": "Ваш запрос требует уточнения. Напишите, пожалуйста, больше деталей.",
            "reply_3": "Ваш запрос обработан. Ожидайте перевода!"
        }
        # Динамически добавляем кнопки
        for key, value in replies.items():
            keyboard.add(types.InlineKeyboardButton(text=value[:30] + "...", callback_data=f"{key}_{user_id}"))

        bot.send_message(
            chat_id=call.message.chat.id,
            text="📋 *Выберите готовый ответ для пользователя:*",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
    def handle_selected_reply(call):
        """Отправка выбранного заготовленного ответа пользователю."""
        data = call.data.split("_")
        reply_key = f"{data[0]}_{data[1]}"  # Ключ с типом ответа
        user_id = int(data[-1])  # ID пользователя

        replies = {
            "reply_1": "Мы приняли ваш запрос. Ожидайте обработки.",
            "reply_2": "Ваш запрос требует уточнения. Напишите, пожалуйста, больше деталей.",
            "reply_3": "👋 *Здравствуйте!* Ваш запрос был принят. Ожидайте, через несколько минут с вами свяжется свободный менеджер.\n\n"
"⚠️ Все сделки проводятся *строго через гарант-сервис*:\n👉 [@WTSGuarantedBOT](https://t.me/WTSGuarantedBOT)"
        }

        # Отправка выбранного ответа пользователю
        bot.send_message(
            chat_id=user_id,
            text=f"📩 *Ответ от менеджера:*\n{replies[reply_key]}",
            parse_mode="Markdown"
        )
        bot.send_message(
            chat_id=MANAGER_ID,
            text="✅ Заготовленный ответ отправлен пользователю.",
            parse_mode="Markdown"
        )