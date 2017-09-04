#!/usr/bin/python
import sqlite3
import os

APP_ROOT = os.path.dirname(os.path.dirname(__file__))


class DB:

    def __init__(self):
        self.version = sqlite3.version
        self.conn = sqlite3.connect(os.path.join(APP_ROOT, "db.db"))
        print("DB has been opened")
        self.cursor = self.conn.cursor()

    def executeSQL(self, command, values):
        return self.cursor.executemany(command, values).fetchall()

    def displayVersion(self):
        print("DB version: ", self.version)

    def addProfile(self, name, email, token, preferences):
        userEmail = "select * from USERS where EMAIL= ?"
        if len(self.executeSQL(userEmail, email)) == 0:
            print("No record found with that email")

            add = "insert into USERS (name, email, token, preferences) VALUES (?,?,?,?)"
            values = [(name, email, token, preferences)]
            self.executeSQL(add, values)
            self.conn.commit()
            print("A new record was be added")
        else:
            print("A record with that email has already been registered")