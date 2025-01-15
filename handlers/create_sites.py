from telebot import types

MANAGER_ID = 7016453953  # ID менеджера


def register_create_sites_subhandlers(bot):
    """Обработчики для всех подтипов создания сайта."""

    @bot.message_handler(func=lambda message: message.text == "🌐 Создание сайтов")
    def handle_sites_creation(message):
        """Отправляем главное сообщение с выбором типов сайтов."""
        bot.send_message(
            chat_id=message.chat.id,
            text=(
                "🌐 *Создание сайтов*\n\n"
                "Мы предлагаем создание профессиональных сайтов, разработанных под ваши нужды.\n\n"
                "*🎯 Возможности сайтов:*\n"
                "- Интернет-магазины.\n"
                "- Корпоративные сайты.\n"
                "- Лэндинги.\n"
                "- Магазины для Instagram.\n"
                "- Персональные блоги.\n\n"
                "*👇 Выберите нужный тип сайта ниже:*"
            ),
            parse_mode="Markdown",
            reply_markup=create_main_inline_keyboard()
        )

    def create_main_inline_keyboard():
        """Создаём главное меню выбора типа сайта."""
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text="🛒 Интернет-магазин", callback_data="site_internet_shop"),
            types.InlineKeyboardButton(text="📷 Instagram Shop", callback_data="site_instagram_shop"),
            types.InlineKeyboardButton(text="🌍 Веб-сайт – о компании", callback_data="site_web_city"),
            types.InlineKeyboardButton(text="💻 Персональный блог", callback_data="site_personal_blog"),  # Новая кнопка
        ]
        keyboard.add(*buttons)
        return keyboard

    def create_back_and_order_keyboard():
        """Создаём inline-кнопки: Назад и Заказать услугу."""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(text="⬅ Назад", callback_data="create_sites_menu"),
            types.InlineKeyboardButton(text="💼 Заказать услугу", callback_data="order_service")
        )
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data.startswith("site_") or call.data == "order_service")
    def handle_inline_sites_options(call):
        """Обработка выбора опций и кнопки 'Заказать услугу'."""
        if call.data == "site_internet_shop":
            bot.send_message(
                chat_id=call.message.chat.id,
                text=(
                    "🛒 *Интернет-магазин*\n\n"
                    "Мы создаём профессиональные интернет-магазины с:\n\n"
                    "📦 Удобным каталогом товаров.\n"
                    "🛒 Интеграцией корзины и оплат.\n"
                    "📊 Отчётностью и аналитикой.\n"
                ),
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "site_instagram_shop":
            bot.send_message(
                chat_id=call.message.chat.id,
                text=(
                    "📷 *Instagram Shop*\n\n"
                    "Создаём магазин, идеально адаптированный для Instagram:\n\n"
                    "🎨 Уникальный дизайн под вашу страничку.\n"
                    "🛍 Упрощение взаимодействия с клиентами.\n"
                    "📈 Возможность интеграции с прочими платформами.\n"
                ),
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "site_web_city":
            bot.send_message(
                chat_id=call.message.chat.id,
                text=(
                    "🌍 *Корпоративный сайт*\n\n"
                    "Разработка сайтов для бизнеса, включающая:\n\n"
                    "🎯 SEO-оптимизация для привлечения трафика.\n"
                    "📱 Мобильную адаптацию.\n"
                    "💼 Отражение вашего бренда и его имиджа.\n"
                ),
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "site_personal_blog":  # Обработка нового пункта
            bot.send_message(
                chat_id=call.message.chat.id,
                text=(
                    "💻 *Персональный блог*\n\n"
                    "Предлагаем разработку вашего индивидуального блога:\n\n"
                    "📝 Уникальный дизайн, отражающий вашу личность.\n"
                    "📚 Удобная структура хранения статей.\n"
                    "🌟 SEO-оптимизация для продвижения в интернете.\n"
                ),
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "create_sites_menu":
            bot.send_message(
                chat_id=call.message.chat.id,
                text="⬅ *Главное меню создания сайтов:*\n\nВыберите нужный тип сайта ниже:",
                parse_mode="Markdown",
                reply_markup=create_main_inline_keyboard()
            )
        elif call.data == "order_service":
            bot.send_message(
                chat_id=call.message.chat.id,
                text=(
                    "📝 *Напишите, пожалуйста, ТЗ (техническое задание), и оно будет отправлено менеджеру.*\n\n"
                    "Ваши ответы можно начинать прямо сейчас."
                ),
                parse_mode="Markdown"
            )

            # Переключаемся в режим "ожидания ответа от пользователя"
            bot.register_next_step_handler_by_chat_id(
                call.message.chat.id, handle_user_tz_submission
            )

    def handle_user_tz_submission(message):
        """Обработка сообщения пользователя с ТЗ."""
        user_tz = message.text
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ *Ваше ТЗ успешно отправлено менеджеру!*\nОжидайте, он скоро свяжется с вами.",
            parse_mode="Markdown"
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_to_user_{message.chat.id}"))

        bot.send_message(
            chat_id=MANAGER_ID,
            text=f"📩 *Новое ТЗ от пользователя:*\n"
                 f"👤 Пользователь: @{message.from_user.username or 'Нет ника'}\n"
                 f"💬 Текст ТЗ:\n{user_tz}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_to_user_"))
    def handle_reply_to_user(call):
        """Менеджер нажимает кнопку 'Ответить', вводит текст ответа."""
        user_id = int(call.data.split("_")[-1])  # Извлекаем ID пользователя из callback_data
        bot.send_message(
            chat_id=call.message.chat.id,
            text="✉️ *Введите текст ответа для пользователя.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, lambda msg: send_reply_to_user(msg, user_id))

    def send_reply_to_user(message, user_id):
        """Отправка ответа от менеджера пользователю."""
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