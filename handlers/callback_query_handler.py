import json
import logging
from utils import InlineMarkupBuilder, Donation


def callback_query_handler(bot, update):
    json_data = json.loads(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    donation_id = json_data["id"]
    cmd = json_data["cmd"]
    logging.info("Received callback command {} from user {} for donation id {}".format(cmd, user_id, donation_id))

    markup_handlers = {
        "to_initial": lambda x, y, z: InlineMarkupBuilder.build_initial_markup(donation_id),
        "payment_step": lambda x, y, z: InlineMarkupBuilder.build_payment_step_markup(donation_id),
        "sum_step": sum_step_handler,
        "set_sum": set_sum_handler,
        "to_payment": lambda x, y, z: InlineMarkupBuilder.build_payment_markup(donation_id),
        "to_sum": lambda x, y, z: InlineMarkupBuilder.build_sum_markup(donation_id),
        "to_main": main_handler,
        "set_payment": set_payment_handler
    }
    if cmd in markup_handlers:
        markup = markup_handlers[cmd](user_id, donation_id, json_data)
        update_markup(update, markup)
    elif cmd == "show_donation":
        show_donation_handler(bot, update)


def update_markup(update, markup):
    update.callback_query.message.edit_reply_markup(reply_markup=markup)
    update.callback_query.answer("")


def sum_step_handler(user_id, donation_id, json_data):
    session = Donation.get_session(user_id, donation_id)
    session.payment_system = json_data["v"]
    return InlineMarkupBuilder.build_sum_markup(donation_id)


def set_sum_handler(user_id, donation_id, json_data):
    session = Donation.get_session(user_id, donation_id)
    session.sum = json_data["v"]
    return InlineMarkupBuilder.build_main_markup(session)


def main_handler(user_id, donation_id, json_data):
    session = Donation.get_session(user_id, donation_id)
    return InlineMarkupBuilder.build_main_markup(session)


def set_payment_handler(user_id, donation_id, json_data):
    session = Donation.get_session(user_id, donation_id)
    session.payment_system = json_data["v"]
    return InlineMarkupBuilder.build_main_markup(session)

def show_donation_handler(bot, update):
    json_data = json.loads(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    donation_id = json_data["id"]
    stub_donations = [
        {"payment_system": "Мобильник", "sum": 1000, "spent": [
            {"sum": 1000, "for": "На дело"}
        ]},
        {"payment_system": "Элсом", "sum": 2000, "spent": [
            {"sum": 500, "for": "Туда"},
            {"sum": 1000, "for": "Сюда"}
        ]},
        {"payment_system": "Мобильник", "sum": 500, "spent": []}
    ]
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=make_donation_message(stub_donations[int(donation_id)])
    )
    update.callback_query.answer("")


def make_donation_message(donation_info):
    message_template = """
Платежная система: {}
Сумма: {}
-----------------------------------

Траты:
{}
"""
    spending_template = """----------
Сумма: {}
На что: {}
"""
    spendings = ''.join(
        [spending_template.format(s["sum"], s["for"])
            for s in donation_info["spent"]])
    return message_template.format(
        donation_info["payment_system"],
        donation_info["sum"],
        spendings
    )
