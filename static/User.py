from collections import defaultdict


class User:

    def __init__(self, name, email, pin):
        self.name = name
        self.email = email
        self.spotifytoken = None
        self.facepath = None
        self.pin = pin
        self.twittertoken = None
        self.maps = False
        self.calendar = False
        self.time=False

    def setName(self, name):
        self.name = name

    def setEmail(self, email):
        self.email = email

    def setSpotifyToken(self, token):
        self.spotifytoken = token

    def setFacePath(self, path):
        self.facepath = path
    def setMaps(self, wantsMaps):
        self.maps = wantsMaps
    def setCalendar(self, wantsCalendar):
        self.calendar = wantsCalendar
    def setPin(self, pin):
        self.pin = self.encode(pin)

    def setTwitterToken(self, token):
        self.twittertoken = token

    def setTime(self,wantsTime):
        self.time=wantsTime