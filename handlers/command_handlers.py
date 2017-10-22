from utils import InlineMarkupBuilder, Donation


def mydonations_handler(bot, update):
    markup = InlineMarkupBuilder.build_mydonations_markup()
    bot.send_message(
        chat_id=update.message.chat.id,
        text="Выберите пожертвование",
        reply_markup=markup)
