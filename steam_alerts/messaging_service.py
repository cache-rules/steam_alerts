# Copyright 2015 jydo inc. All rights reserved.
import random
from twilio.rest import TwilioRestClient
from steam_alerts import logger
from steam_alerts.person import Person


class MessagingService:
    def __init__(self, sid, auth_token, twilio_number, messages):
        self.client = TwilioRestClient(sid, auth_token)
        self.twilio_number = twilio_number
        self.messages = messages

    def send_message(self, player: Person, game_name):
        msg = random.choice(self.messages).format(game=game_name)
        logger.info('Sending message "{}" to {}'.format(msg, player.name))
        self.client.messages.create(body=msg, to=player.phone_number, from_=self.twilio_number)


class MockMessagingService(MessagingService):
    def send_message(self, player: Person, game_name):
        msg = random.choice(self.messages).format(game=game_name)
        logger.info('Sending message "{}" to {}'.format(msg, player.name))