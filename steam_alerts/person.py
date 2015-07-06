# Copyright 2015 jydo inc. All rights reserved.


class Person:
    def __init__(self, name, phone_number, steam_id):
        self.name = name
        self.phone_number = phone_number
        self.steam_id = steam_id
        self.persona_state = None
        self.game = None
        self.last_messaged = None
