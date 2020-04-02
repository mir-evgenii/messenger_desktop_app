import requests
import json
import datetime

from model import model

class API:

    def __init__(self):

        self.model = model()

        self.api = json.load(open("API.json"))
        self.url = "{}{}{}".format(self.api['host'], self.api['port'], self.api['url'])
        self.key = '123'
        self.name = 'User 1'

        response=requests.get(self.url.format('client')+self.api['add_client'].format(self.key))
        #print(response.text)

    def get_contact_list(self):

        contacts = self.model.get_contacts()

        keys = ''
        for contact in contacts:
            keys = keys + contact[2] + ';'

        response=requests.get(self.url.format('client')+self.api['get_online_clients'].format(keys))
        #print(response.text)
        online_contacts = json.loads(response.text)

        contacts_list = []
        for contact in contacts:
            if (contact[2] in online_contacts['online_users']):
                contacts_list.append(contact[1] + ' (online)')
            else:
                contacts_list.append(contact[1] + ' (offline)')

        return contacts_list

    def get_chat(self, cont='User 2 (offline)'):

        # перенести в демон для получения сообщений и запись в базу
        # response=requests.get(self.url.format('message') + self.api['get_messages'].format(self.key))
        # response=requests.get(self.url.format('message')+self.api['get_messages'].format('345'))
        # self.model.set_messages(json.loads(response.text))

        # удаление online/offline из имени контакта
        cont = ' '.join(cont.split()[0:-1])

        contact = self.model.get_contact(cont)

        messages = self.model.get_messages(self.key, contact[2])

        chat = []
        for message in messages:
            if (message[1] == self.key):
                chat.append([self.name, message[3]])
            else:
                chat.append([contact[2], message[3]])
        return chat

    def send_message(self, message, recipient = '345'):

        response=requests.get(self.url.format('message') + self.api['send_message'].format(message, self.key, recipient))
        print(response.text)

        time = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        self.model.set_message(message, self.key, recipient, time)


    def get_contact(self, cont):
        # print(cont)
        return self.get_chat(cont)

    # добавить деструктор с выходом в оффлайн!!!

    # def send_key(self):
    #     response = requests.get('http://localhost/index.php?r=client/add-client&key=123', verify=False)
    #     print(response.text)
