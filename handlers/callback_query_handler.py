import json
import logging
from utils import InlineMarkupBuilder, Donation


def callback_query_handler(bot, update):
    json_data = json.loads(update.callback_query.data)
    user_id = update.callback_query.from_user.id
    donation_id = json_data["id"]
    cmd = json_data.get("cmd", "to_initial")
    logging.info("Received callback command {} from user {} for donation id {}".format(cmd, user_id, donation_id))

    handlers = {
        "to_initial": lambda x, y, z: InlineMarkupBuilder.build_initial_markup(donation_id),
        "payment_step": lambda x, y, z: InlineMarkupBuilder.build_payment_step_markup(donation_id),
        "sum_step": sum_step_handler,
        "set_sum": set_sum_handler,
        "to_payment": lambda x, y, z: InlineMarkupBuilder.build_payment_markup(donation_id),
        "to_sum": lambda x, y, z: InlineMarkupBuilder.build_sum_markup(donation_id),
        "to_main": main_handler,
        "set_payment": set_payment_handler
    }
    markup = handlers[cmd](user_id, donation_id, json_data)
    update_markup(update, markup)


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

