import requests
import json
import datetime

from model import model
from sign import sign

class API:

    def __init__(self):

        self.model = model()
        self.sign = sign()

        self.api = json.load(open("API.json"))
        self.url = "{}{}{}".format(self.api['host'], self.api['port'], self.api['url'])
        self.conf = json.load(open("conf.json"))

        public_key = 'bob_public_rsa_key.pem'
        self.key = open(public_key).read()
        #self.key = self.conf['key']
        self.name = self.conf['name']

        response=requests.get(self.url.format('client')+self.api['add_client'].format(self.key))
        print(response.text)

    def get_contact_list(self):

        self.get_messages()

        contacts = self.model.get_contacts()

        keys = ''
        for contact in contacts:
            keys = keys + contact[2] + ';'

        response=requests.get(self.url.format('client')+self.api['get_online_clients'].format(keys))
        print(response.text)
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
        response = requests.get(self.url.format('message') + self.api['get_messages'].format(self.key))
        print(response.text)
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

        str_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        #sign = self.sign.sign_message(str(str_datetime) + ' ' + message)
        sign = self.sign.sign_message(message)

        response=requests.get(self.url.format('message') + self.api['send_message'].format(message, self.key, recipient, str(str_datetime), sign))
        print(response.text)

        self.model.set_message(message, self.key, recipient, time)

    def get_contact(self, cont):
        return self.get_chat(cont)

    def __del__(self):
        response=requests.get(self.url.format('client')+self.api['del_client'].format(self.key))
        print(response.text)

