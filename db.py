#!/usr/bin/python
import sqlite3
from static import User
from werkzeug.exceptions import BadRequest


# Database class which will be used to connect or execute commands in the DB


class DB:
    # Initializing the class with some class variables
    def __init__(self, root):
        self.root = root
        self.version = sqlite3.version
        self.conn = sqlite3.connect(root + "\DATA.db")
        print(root + "\DATA.db")
        print("DB has been opened")
        self.cursor = self.conn.cursor()

    def displayVersion(self):
        print("DB version: ", self.version)

    def insertUserData(self, user):
        add = "INSERT INTO USERS (name, email, googletoken, pin, facepath, spotifytoken, twittertoken) VALUES (?,?,?,?,?,?,?)"
        self.conn.executemany(add, [(user.name, user.email, user.googletoken, user.pin,
                                     user.facepath, user.spotifytoken, user.twittertoken)])
        self.conn.commit()

    # Adds a profile to the DB if it does not exists
    def addProfile(self, content):
        try:
            user = self.createUser(content)
        except BadRequest as e:
            print(e.description)
            raise e

        if not self.isUserRegistered(user):
            self.insertUserData(user)
            print("A new record was be added")
        else:
            # We need to return something to the API end point here so it can display a
            # message in the UI
            raise BadRequest("A record with that email has already been registered")

    def isUserRegistered(self, user):

        userByEmail = 'SELECT COUNT(*) FROM USERS WHERE EMAIL= ?'
        count = self.conn.execute(userByEmail, [user.email]).fetchone()[0]
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def createUser(content):
        try:
            user = User.User(content["name"], content["email"], content["googletoken"], content["pin"])
        except KeyError as e:
            raise BadRequest("I/O error: {0} was not included".format(e))
        try:
            user.setSpotifyToken(content["spotifytoken"])
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.setTwitterToken(content["twittertoken"])
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))

        return user
