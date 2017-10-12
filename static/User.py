from collections import defaultdict


class User:

    def __init__(self, name, email, pin):
        self.name = name
        self.email = email
        self.pin = pin
        self.home = ""
        self.work = ""
        self.weatherwidget = False
        self.twitterwidget = False
        self.mapswidget = False
        self.calendarwidget = False
        self.clockwidget=False
