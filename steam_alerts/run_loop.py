# Copyright 2015 jydo inc. All rights reserved.
import json
import time
from steam_alerts import logger
from steam_alerts.messaging_service import MessagingService, MockMessagingService
from steam_alerts.person import Person
from steam_alerts.steam_service import SteamService, status_types


def run_loop(config_path):
    with open(config_path) as file:
        config = json.load(file)

    steam_key = config['steam_key']
    twilio_sid = config['twilio_sid']
    twilio_auth_token = config['twilio_auth_token']
    twilio_number = config['twilio_number']
    poll_rate = config.get('poll_rate', 60)
    message_rate = config.get('message_rate', 60 * 5)
    messages = config['messages']
    players = {}

    messaging_service = MessagingService(twilio_sid, twilio_auth_token, twilio_number, messages)
    steam_service = SteamService(steam_key)

    for player_json in config['players']:
        if player_json['phone_number'] != "" and player_json['steam_id'] != "":
            person = Person(**player_json)
            logger.info("Adding {}".format(person.name))
            players[person.steam_id] = person

    logger.info('Starting run loop.')
    while True:
        statuses = steam_service.get_player_statuses(','.join(players.keys()))

        for status in statuses:
            person = players[status['steamid']]
            persona_state = status['personastate']
            old_state = status_types.get(person.persona_state, None)
            new_state = status_types[persona_state]
            old_game = person.game
            new_game = status.get('gameextrainfo')
            person.persona_state = persona_state
            person.game = new_game
            msg = '{} is {}'.format(person.name, new_state)
            can_send = person.last_messaged is None or ((time.time() - person.last_messaged) >= message_rate)

            if new_game is not None:
                msg += ' and is playing "{}"'.format(new_game)
            else:
                msg += ' and not in a game'

            if old_state != new_state or new_game != old_game:
                logger.info(msg)

            if person.game is not None and can_send:
                if 'thomas' in person.game.lower():
                    messaging_service.send_message(person)
                    person.last_messaged = time.time()

        time.sleep(poll_rate)
