import tkinter
import tkinter.messagebox

from API import API
from model import model

class GUI:

    def __init__(self):

        self.readme = '''

        Добро пожаловать!
        ---------------------
        Версия месседжера 0.1

        В данной версии возможно отправлять сообщения.
        Сообщения сохраняются в локальной базе данных.

        Больше информации на сайте: http://....

        '''

        # Создаем основное окно
        self.root = tkinter.Tk()
        self.root.minsize(width=500,height=300)
        self.root.geometry("750x500")
        self.root.title("Messenger")

        self.api = API()
        self.model = model()

        # При первом открытии мессенджера фрейма для ввода сообщения нет
        # поскольку в меню не выбран контакт которому отправляем сообщение
        # после выбора контакта появляется фрейм
        self.send_message_frame_not_view = True

        # Создаем меню
        self.menu()

        # Создаем фрейм со списком контактов
        self.contact_frame()

        # Создаем фрейм с чатом
        self.message_frame()

        # Выводим основное окно
        self.root.mainloop()

    def del_online_offline_simbol(self, contact):
        '''
        Удаление offline/online символа из имени контакта
        '''
        contact = ' '.join(contact.split()[1:])
        return contact


    def send_message(self, event):
        '''
        Метод для отправки сообщения
        '''

        contact = self.contact_listbox.get(self.contact_listbox.curselection())
        # удаление online/offline из имени контакта
        contact = self.del_online_offline_simbol(contact)

        recipient = self.model.get_contact(contact)

        message = self.send_message_text.get("1.0", tkinter.END)
        self.api.send_message(message, int(recipient[2]))
        self.get_chat(event)

    def get_chat(self, event):
        contact = self.contact_listbox.get(self.contact_listbox.curselection())
        contact = self.del_online_offline_simbol(contact)
        msgs = self.api.get_contact(contact)
        self.chat_text.destroy()
        self.chat_text = tkinter.Text(self.chat_frame, width=50, height=15, font="Arial 9")
        txt_msg = self.parse_chat(msgs)
        self.chat_text.insert(tkinter.CURRENT, txt_msg)
        self.chat_text.config(state=tkinter.DISABLED)
        self.chat_text.yview(tkinter.END)
        self.chat_text.pack(expand=1, fill=tkinter.BOTH)

        if (self.send_message_frame_not_view):
            self.send_message_frame()

    def contact_frame(self):
        '''
        Метод для отображения списка контактов
        '''

        # Создаем фрейм для списка контактов
        self.contacts_frame = tkinter.Frame(self.root)
        self.contacts_frame.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # Создаем и выводим список контактов
        contact_list = self.api.get_contact_list()
        self.contact_listbox = tkinter.Listbox(self.contacts_frame, selectmode=tkinter.SINGLE, height=6)
        for contact in contact_list:
            self.contact_listbox.insert(tkinter.END, contact)
        self.contact_listbox.bind('<<ListboxSelect>>', self.get_chat)
        self.contact_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

    def parse_chat(self, chat_list):
        text_chat = ''
        for message in chat_list:
            text_chat = text_chat + message[0] + ':\n ' + message[1] + '\n'
        return text_chat

    def message_frame(self):
        '''
        Метод для отображения фрейма чата
        '''

        # Создаем основной фрейм чата
        self.main_chat_frame = tkinter.Frame(self.root)
        self.main_chat_frame.pack(expand=1, side=tkinter.LEFT, fill=tkinter.BOTH)

        # Создаем фрейм чата для вывода сообщений
        self.chat_frame = tkinter.Frame(self.main_chat_frame)
        self.chat_frame.pack(expand=1, fill=tkinter.BOTH)

        self.chat_text = tkinter.Text(self.chat_frame, width=20, height=5, font="Arial 9")
        self.chat_text.insert(tkinter.CURRENT, self.readme)
        self.chat_text.config(state=tkinter.DISABLED)
        self.chat_text.pack(expand=1, fill=tkinter.BOTH)

    def send_message_frame(self):
        '''
        Метод для отображения поля ввода сообщения
        '''

        # Создаем поле для ввода сообщения
        self.send_message_text_frame = tkinter.Frame(self.main_chat_frame)
        self.send_message_text_frame.pack(side=tkinter.LEFT, expand=1, fill=tkinter.X)

        self.send_message_text = tkinter.Text(self.send_message_text_frame, width=40, height=1, font="Arial 9")
        self.send_message_text.bind("<Return>", self.send_message)
        self.send_message_text.pack(expand=1, fill=tkinter.X)

        # Создаем кнопку отправки сообщения
        self.send_message_btn_frame = tkinter.Frame(self.main_chat_frame)
        self.send_message_btn_frame.pack(side=tkinter.LEFT)

        self.send_message_btn = tkinter.Button(self.send_message_btn_frame, text="\u27A4", font="Arial 5")
        self.send_message_btn.bind("<Button-1>", self.send_message)
        self.send_message_btn.pack()

        self.send_message_frame_not_view = False

    def menu(self):
        self.main_menu = tkinter.Menu(self.root)
        self.root.config(menu=self.main_menu)

        fm = tkinter.Menu(self.main_menu, tearoff=0) # создается пункт меню с размещением на основном меню (m)
        self.main_menu.add_cascade(label="\u2261",menu=fm) #пункту располагается на основном меню (m)
        fm.add_command(label="Контакты", command=self.add_contact) #формируется список команд пункта меню
        fm.add_command(label="Настройки")
        fm.add_command(label="О программе")

        #hm = tkinter.Menu(self.main_menu, tearoff=0) #второй пункт меню
        #self.main_menu.add_cascade(label="Помощь",menu=hm)
        #hm.add_command(label="Помощь")
        #hm.add_command(label="О программе")

    def add_contact(self):
        '''
        Создание окна управления контактами
        '''

        self.add_contact_win = tkinter.Toplevel(self.root)
        self.add_contact_win.title('Контакты')
        self.add_contact_win.minsize(width=400,height=200)
