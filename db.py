#!/usr/bin/python
import sqlite3
import hashlib

from flask import jsonify
import json

from static.User import User
from werkzeug.exceptions import BadRequest


# Database class which will be used to connect or execute commands in the DB


class DB:
    # Initializing the class with some class variables
    def __init__(self, root):
        self.root = root
        self.version = sqlite3.version
        self.conn = sqlite3.connect(root + "/DATA.db", check_same_thread=False)
        print("DB has been opened")
        self.cursor = self.conn.cursor()

    def displayVersion(self):
        print("DB version: ", self.version)

    # Sets the information given by the user to the DB
    def insertUserData(self, user):
        add = "INSERT INTO USERS (name, email, facePath, pin, calendarWidget, twitterWidget, mapWidget, clockWidget, weatherWidget, homeAddess, workAddress) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        self.conn.executemany(add, [(user.name, user.email,"-" ,user.pin,
                                     user.calendarwidget, user.twitterwidget, user.mapswidget, user.clockwidget, user.weatherwidget, user.home,user.work)])
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
            print("A new profile has been added")
        else:
            raise BadRequest("A record with that email has already been registered")

    def isUserRegistered(self, email):

        userByEmail = 'SELECT COUNT(*) FROM USERS WHERE EMAIL= ?'
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
            user.home = content["homeAddress"]
        except KeyError as e:
            print("I/O error: {0} was not included".format(e))
        try:
            user.work = content["workAddress"]
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
        hasheddpin = self.getHashedPin(email)
        isSame = self.isHashSame(hasheddpin, pin)
        if isSame:
            query = "DELETE FROM USERS WHERE email = ?"
            self.conn.execute(query, [email])
            self.conn.commit()
        else:
            raise BadRequest

    def getUser(self, email):
        if self.isUserRegistered(email):
            query = "SELECT * FROM USERS WHERE email = ?"
            userData = self.conn.execute(query, [email]).fetchall()[0]
            userData = list(userData)
            print(userData)
            preferences = {"email":userData[0],
                                   "name":userData[1],
                                   "facepath":"-",
                                   "pin":userData[3],
                                   "calendarWidget":userData[4],
                                   "mapWidget":userData[5],
                                   "twitterWidget":userData[6],
                                   "clockWidget":userData[7],
                                   "weatherWidget":userData[8],
                                   "homeAddress":userData[9],
                                   "workAddress":userData[10]}
            return preferences
        else:
            raise BadRequest

    def setEvents(self, title, status, startTime, endTime, email):
        query = "INSERT INTO Events (title, status, startTime, endTime) VALUES (?,?,?,?) "
        self.conn.executemany(query, [(title, status, startTime, endTime)])
        self.conn.commit()
        eventID = self.conn.execute("SELECT MAX(eventID) from Events").fetchall()
        eventID = int(eventID[0][0])
        query = "INSERT INTO Participants (email, eventID) VALUES (?,?)"
        self.conn.executemany(query, [(email, eventID)])
        self.conn.commit()

    def getHashedPin(self, email):
        query = "SELECT * FROM USERS WHERE email = ?"
        pin = ''
        try:
            pin = self.conn.execute(query, [email]).fetchone()[3]
        except Exception as e:
            raise BadRequest("")
        return pin

    def getEvents(self,email):

        query = "SELECT eventID from Participants where email = ?"
        eventIDs = self.conn.execute(query,[email]).fetchall()
        events = []
        sql = "select * from Events WHERE eventID = ?"
        for id in eventIDs:
            _list = self.conn.execute(sql, [id[0]]).fetchone()
            event = {"Title":_list[1],
                     "startTime":_list[3],
                     "endTime":_list[4],
                     "status":_list[2]}
            events.append(event)
        if len(events) < 1:
            return jsonify({"Error":"This user does not have any events saved in Google"})
        return jsonify(events)

    @staticmethod
    def getEmail(self):
        query = "SELECT email FROM Users"
        emails = self.conn.execute(query)
        return emails

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
