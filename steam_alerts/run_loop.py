# Copyright 2015 jydo inc. All rights reserved.
import json
import time
from steam_alerts import logger
from steam_alerts.messaging_service import MessagingService
from steam_alerts.person import Person
from steam_alerts.steam_service import SteamService

status_types = {
    0: 'Offline',
    1: 'Online',
    2: 'Busy',
    3: 'Away',
    4: 'Snooze',
    5: 'Looking to trade',
    6: 'Looking to play'
}


def run_loop(config_path):
    with open(config_path) as file:
        config = json.load(file)

    steam_key = config['steam_key']
    twilio_sid = config['twilio_sid']
    twilio_auth_token = config['twilio_auth_token']
    twilio_number = config['twilio_number']
    messages = config['messages']
    players = {}

    messaging_service = MessagingService(twilio_sid, twilio_auth_token, twilio_number, messages)
    steam_service = SteamService(steam_key)

    for player_json in config['players']:
        if player_json['phone_number'] != "" and player_json['steam_id'] != "":
            player = Person(**player_json)
            logger.info("Adding {}".format(player.name))
            players[player.steam_id] = player

    logger.info('Starting run loop.')
    while True:
        statuses = steam_service.get_player_statuses(','.join(players.keys()))

        for status in statuses:
            player = players[status['steamid']]
            persona_state = status['personastate']

            logger.info('{} is "{}"'.format(player.name, status_types[persona_state]))

            if persona_state == 1:
                if 'gameextrainfo' in status:
                    game = status['gameextrainfo']
                    logger.info('{} is in a game: "{}"'.format(player.name, game))

                    if 'dota' in game.lower():
                        logger.info('{} is playing DOTA, annoy them!'.format(player.name))
                        messaging_service.send_message(player)
                else:
                    logger.info('{} is not in a game.'.format(player.name))

        time.sleep(60 * 10)
