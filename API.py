import requests
import json
import datetime
import logging

from model import model
from sign import sign

class API:

    def __init__(self):

        self.model = model()
        self.sign = sign()

        self.api = json.load(open("API.json"))
        self.url = self.api['host'] + self.api['port']
        self.conf = json.load(open("conf.json"))

        self.key = self.conf['key']
        self.name = self.conf['name']

        # Настройка логирования
        logging.basicConfig(filename="logs/app.log", filemode="w", level=logging.INFO)

        self.online()

    def online(self):
        payload = {'key': self.key}
        response=requests.get(self.url + self.api['add_client'], params = payload)
        self.log_response(response)

    def log_response(self, response):
        if (response.status_code == 200):
            logging.info('SUCCESS:\n request: {}\n response: {}\n'.format(response.url, response.text))
        elif (response.status_code != 200):
            logging.info('ERROR:\n request: {}\n response code: {}\n'.format(response.url, response.status_code))
            exit()


    def get_contact_list(self):

        self.get_messages()

        contacts = self.model.get_contacts()

        keys = ''
        for contact in contacts:
            keys = keys + contact[2] + ';'

        payload = {'keys': keys}
        response=requests.get(self.url + self.api['get_online_clients'], params = payload)
        self.log_response(response)
        online_contacts = json.loads(response.text)

        contacts_list = []
        for contact in contacts:
            count_new_messages = self.model.get_count_new_messages(contact[2])
            count_new_messages = count_new_messages[0]
            if (contact[2] in online_contacts['online_users']):
                # + online
                if (count_new_messages == 0):
                    contacts_list.append('\u002B ' + contact[1])
                else:
                    contacts_list.append('\u002B{} '.format(count_new_messages) + contact[1])
            else:
                # x offline
                if (count_new_messages == 0):
                    contacts_list.append('\u00D7 ' + contact[1])
                else:
                    contacts_list.append('\u00D7{} '.format(count_new_messages) + contact[1])

        return contacts_list

    def get_messages(self):
        payload = {'key': self.key}
        response = requests.get(self.url + self.api['get_messages'], params = payload)
        self.log_response(response)
        online_contacts = json.loads(response.text)
        self.model.set_messages(json.loads(response.text))

    def get_chat(self, cont):

        contact = self.model.get_contact(cont)

        messages = self.model.get_messages(contact[2])

        chat = []
        for message in messages:
            if (message[1] == self.key):
                chat.append([self.name, message[3]])
            else:
                chat.append([contact[1], message[3]])
        return chat

    def send_message(self, message, recipient):

        str_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #sign = self.sign.sign_message(str(str_datetime) + ' ' + message)
        sign = self.sign.sign_message(message)

        payload = {'message': message, 'key': self.key, 'recipient': recipient, 'date': datetime, 'sign': sign}

        response=requests.get(self.url + self.api['send_message'], params = payload)
        self.log_response(response)

        self.model.set_message(message, self.key, recipient, time)

    def get_contact(self, cont):
        return self.get_chat(cont)

    def __del__(self):
        payload = {'key': self.key}
        response=requests.get(self.url+self.api['del_client'], params = payload)
        self.log_response(response)

