#!/usr/bin/python
import sqlite3
import hashlib
from static.User import User
from werkzeug.exceptions import BadRequest


# Database class which will be used to connect or execute commands in the DB


class DB:
    # Initializing the class with some class variables
    def __init__(self, root):
        self.root = root
        self.version = sqlite3.version
        self.conn = sqlite3.connect(root + "\DATA.db", check_same_thread=False)
        print("DB has been opened")
        self.cursor = self.conn.cursor()

    def displayVersion(self):
        print("DB version: ", self.version)

    # Sets the information given by the user to the DB
    def insertUserData(self, user):
        add = "INSERT INTO USERS (name, email, facePath,pin, twitterWidget, mapWidget, calendarWidget, clockWidget, weatherWidget) VALUES (?,?,?,?,?,?,?,?,?)"
        self.conn.executemany(add, [(user.name, user.email,"-" ,user.pin,
                                     user.calendarwidget, user.twitterwidget, user.mapswidget, user.calendarwidget,user.clockwidget)])
        self.conn.commit()

    # Adds a profile to the DB if it does not exists
    def addProfile(self, content):
        try:
            user = self.createUser(content)
        except BadRequest as e:
            print(e.description)
            raise e

        if not self.isUserRegistered(user.email):
            self.insertUserData(user)
            print("A new record was be added")
        else:
            raise BadRequest("A record with that email has already been registered")

    def isUserRegistered(self, email):

        userByEmail = 'SELECT COUNT(*) FROM Users WHERE email= ?'
        count = self.conn.execute(userByEmail, [email]).fetchone()[0]
        if count > 0:
            return True
        else:
            return False


    def createUser(self, content):
        print(content)
        try:
            user = User(content["name"], content["email"], DB.encrypt(content["pin"]))
        except KeyError as e:
            raise BadRequest("I/O error: {0} was not included".format(e))
        try:
            user.clockwidget = content["clockwidget"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.twitterwidget= content["twitterwidget"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.calendarwidget=content["calendarwidget"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.mapswidget=content["mapswidget"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.weatherwidget=content["weatherwidget"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))

        return user

    # Hash the pin and compare it with the one on the DB
    # If it is the same go ahead and delete it
    # If it is not the same throw some error
    def deleteUser(self, email, pin):
        if self.isHashSame(self.getHashedPin(email), pin):
            query = "DELETE FROM Users WHERE email = ?"
            self.conn.execute(query, [email])
        else:
            raise BadRequest

    def getUser(self, email):
        if self.isUserRegistered(email):
            query = "SELECT * FROM Users WHERE email = ?"
            userData = list(self.conn.execute(query, [email]).fetchall())
            return userData
        else:
            raise BadRequest


    def getHashedPin(self, email):
        query = "SELECT * FROM Users WHERE email = ?"
        pin = self.conn.execute(query, [email]).fetchone()[2]
        return pin

    @staticmethod
    def encrypt(pin):
        m = hashlib.new('sha512')
        m.update(pin.encode('utf8'))
        return m.hexdigest()

    @staticmethod
    def isHashSame(hashed_pin, original_pin):
        m = DB.encrypt(original_pin)
        if hashed_pin == m:
            return True
        return False
