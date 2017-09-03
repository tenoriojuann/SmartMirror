import os
import sqlite3
class DB:

    def __init__(self):
        self.version = sqlite3.version
        self.conn = sqlite3

    def getCursor(self):
        return self.connectDB(self).cursor()

    def execute(self, command):

        return self.getCursor(self).execute(command).fetchall();

    def connectDB(self):
        return self.conn.connect('static/db.sqlite')

    def displayVersion(self):
        print("DB version: ", self.version)

    def addToken(self, name, email, token, preferences):
        command = "select * from users when email = ?", (email,)
        if len(self.execute(self, command)) == 0:
            print("No record found with that email")
            print("A new record will be added")
            add = "insert into users (?,?,?,?)", (name,email,token,preferences,)
            self.execute(self, add)
        else:
            print("A record with that email has already been registered")