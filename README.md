# steam_alerts
Monitor and annoy your friends via text message when they start playing DOTA.

# Requirements:

* [Steam API key](https://steamcommunity.com/dev/apikey).
* [Twilio](http://www.twilio.com) Account.
* [Python 3.3+](https://www.python.org/downloads/), because it's 2015.
* [Requests](http://docs.python-requests.org/en/latest/).
* [Twilio API client](https://www.twilio.com/docs/python/install).

# Setup:

* Create a virtual environment
* Activate the environment
* Run `pip install requirements.txt`
* Create a `config.json` file that looks something like this:
```JSON
    {
      "steam_key": "YOUR_STEAM_KEY_HERE",
      "twilio_sid": "YOUR_TWILIO_SID_HERE",
      "twilio_auth_token": "YOUR_TWILIO_AUTH_TOKEN_HERE",
      "twilio_number": "YOUR_TWILIO_NUMBER_HERE_WITH_COUNTRY_CODE",
      "debug": false, // Toggles if we send real messages or not. Optional, defaults to false.
      "poll_rate": 60, // Determines how often we hit the Steam APIs. Optional, defaults to 60
      "message_rate": 300, // Determines how often we message someone. Optional, defaults to 300
      "messages": [
        "Hey Dummy, stop playing DOTA.",
        "Looks like you're playing DOTA, stop.",
        "You know, instead of playing DOTA, you could literally be doing anything else.",
        "Stop playing DOTA",
        "You know you're not being paid to play DOTA right?"
      ],
      "players": [{
        "name": "Josh",
        "phone_number": "NUMBER_TO_TEXT_HERE_WITH_COUNTRY_CODE",
        "steam_id": "STEAM_ID_HERE"
      }, {
        "name": "Alan",
        "phone_number": "NUMBER_TO_TEXT_HERE_WITH_COUNTRY_CODE",
        "steam_id": "STEAM_ID_HERE"
      }]
    }
```
## NOTES:

* Phone numbers have to include their country code and can **only** have numbers in them, i.e. 15556667777
* Steam IDs can be found by going to your friend's steam profile and looking at the URL.
    * If they don't have a vanity url it will look like this: `http://steamcommunity.com/profiles/STEAM_ID_HERE/`
    * If they have a vanity URL you can get their Steam ID by using the `SteamService.resolve_vanity_url` method.
    * In the future I'll enable the ability to put a vanity URL in the config file, and we'll auto convert it to a steam id.
