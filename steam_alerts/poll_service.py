# Copyright 2015 jydo inc. All rights reserved.
import json
import time
from steam_alerts import logger
from steam_alerts.messaging_service import MessagingService, MockMessagingService
from steam_alerts.person import Person
from steam_alerts.steam_service import SteamService, status_types


class PollService:
    def __init__(self, config_path):
        with open(config_path) as file:
            config = json.load(file)

        self.steam_key = config['steam_key']
        self.twilio_sid = config['twilio_sid']
        self.twilio_auth_token = config['twilio_auth_token']
        self.twilio_number = config['twilio_number']
        self.poll_rate = config.get('poll_rate', 60)
        self.message_rate = config.get('message_rate', 60 * 5)
        self.messages = config['messages']
        self.debug = config.get('debug', False)
        self.people = {}
        self.steam_service = SteamService(self.steam_key)

        if self.debug:
            self.messaging_service = MockMessagingService(self.twilio_sid, self.twilio_auth_token, self.twilio_number,
                                                          self.messages)
        else:
            self.messaging_service = MessagingService(self.twilio_sid, self.twilio_auth_token, self.twilio_number,
                                                      self.messages)

        for player_json in config['players']:
            if player_json['phone_number'] != "" and player_json['steam_id'] != "":
                person = Person(**player_json)
                logger.info("Adding {}".format(person.name))
                self.people[person.steam_id] = person

    def run_loop(self):
        logger.info('Starting run loop.')
        while True:
            statuses = self.steam_service.get_player_statuses(','.join(self.people.keys()))

            for status in statuses:
                person = self.people[status['steamid']]
                persona_state = status['personastate']
                old_state = status_types.get(person.persona_state, None)
                new_state = status_types[persona_state]
                old_game = person.game
                new_game = status.get('gameextrainfo')
                person.persona_state = persona_state
                person.game = new_game
                msg = '{} is {}'.format(person.name, new_state)
                can_send = person.last_messaged is None or ((time.time() - person.last_messaged) >= self.message_rate)

                if new_game is not None:
                    msg += ' and is playing "{}"'.format(new_game)
                else:
                    msg += ' and not in a game'

                if old_state != new_state or new_game != old_game:
                    logger.info(msg)

                if person.game is not None and can_send:
                    if 'dota' in person.game.lower():
                        self.messaging_service.send_message(person)
                        person.last_messaged = time.time()

            time.sleep(self.poll_rate)

    def start(self):
        self.run_loop()
