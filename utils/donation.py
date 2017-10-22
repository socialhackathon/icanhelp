import json


class Donation:

    sessions = {}

    def get_session(user_id, donation_id):
        if not user_id in Donation.sessions or not donation_id in Donation.sessions[user_id]:
            donation = Donation(donation_id)
            Donation.sessions[user_id] = {donation_id: donation}
        return Donation.sessions[user_id][donation_id]

    def __init__(self, donation_id):
        self.donation_id = donation_id
        self.payment_system = None
        self.sum = 0
        self.payment_system_urls = {
            "mobilnik": "https://demomoney.yandex.ru/to/4100324939028/{}",
            "elsom": "https://demomoney.yandex.ru/to/4100324939028/{}",
            "yandex": "https://demomoney.yandex.ru/to/4100324939028/{}"
        }

    def make_payment_url(self):
        if self.payment_system is not None and self.payment_system in self.payment_system_urls:
            return self.payment_system_urls[self.payment_system].format(self.sum)
