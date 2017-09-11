from collections import defaultdict


class User:

    def __init__(self, name, email, googletoken, pin):
        self.name = name
        self.email = email
        self.googletoken = googletoken
        self.spotifytoken = None
        self.facepath = None
        self.pin = pin
        self.twittertoken = None

    def setName(self, name):
        self.name = name

    def setEmail(self, email):
        self.email = email

    def setGoogleToken(self, token):
        self.googletoken = token

    def setSpotifyToken(self, token):
        self.spotifytoken = token

    def setFacePath(self, path):
        self.facepath = path

    def setPin(self, pin):
        self.pin = self.encode(pin)

    def encode(self, pin):
        # TODO: make an encoding algorithm
        return pin

    def setTwitterToken(self, token):
        self.twittertoken = token