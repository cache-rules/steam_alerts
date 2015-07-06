# Copyright 2015 jydo inc. All rights reserved.
from steam_alerts import PollService


if __name__ == '__main__':
    ps = PollService('./config.json')
    ps.start()
