#!/usr/bin/python
import sqlite3
import os

APP_ROOT = os.path.dirname(os.path.dirname(__file__))

# Database class which will be used to connect or execute commands in the DB

class DB:

# Initializing the class with some class variables
    def __init__(self):
        self.version = sqlite3.version
        self.conn = sqlite3.connect(os.path.join(APP_ROOT, "db.db"))
        print(os.path.join(APP_ROOT, "db.db"))
        print("DB has been opened")
        self.cursor = self.conn.cursor()

    # Method that can be called to execute a command
    def executeSQL(self, command, values):
        return self.cursor.executemany(command, values).fetchall()

    def displayVersion(self):
        print("DB version: ", self.version)

    # Adds a profile to the DB if it does not exists
    # It should make sure to convert 'preferences' to a string and store it or make new columns in DB
    def addProfile(self, name, email, token, preferences):
        userEmail = 'select * from USERS where EMAIL= ?'
        if len(self.executeSQL(userEmail, email)) == 0:
            print("No record found with that email")

            add = "insert into USERS (name, email, spotifytoken, preferences) VALUES (?,?,?,?)"
            values = [(name, email, token, preferences)]
            self.executeSQL(add, values)
            self.conn.commit()
            print("A new record was be added")
        else:
            # We need to return something to the API end point here so it can display a
            # message in the UI
            print("A record with that email has already been registered")