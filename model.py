import sqlite3
import datetime

class model:

    def __init__(self):

        self.conn = sqlite3.connect("clientdb.db")
        self.cursor = self.conn.cursor()

    def set_message(self, message, sender, recipient, time):
        '''
        Запись сообщения в базу
        '''

        self.cursor.execute("INSERT INTO messages VALUES (null, '{}', '{}', '{}', '{}', '{}')".format(sender, recipient, message, time, datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")))

        self.conn.commit()

    def set_messages(self, messages):

        for message in messages['messages-for-client']:
            time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            self.set_message(message['content'], message['sender'], message['recipient'], time)

    def get_messages(self, sender, recipient):

        sql = "SELECT * FROM messages WHERE sender={} AND recipient={}".format(str(sender), str(recipient))
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_contacts(self):

        sql = "SELECT * FROM contacts"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_contact(self, name):

        sql = "SELECT * FROM contacts WHERE name='{}'".format(name)
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def edit_contact(self, contact_id, name, key):
        pass

    def del_contact(self, contact_id):
        pass

    def add_contact(self, name, key):

        sql = "INSERT INTO contacts VALUES (null, '{}', '{}', null)".format(name, key)
        self.cursor.execute(sql)
        self.conn.commit()


