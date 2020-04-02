import tkinter
import tkinter.messagebox

from API import API

class GUI:

    def __init__(self):

        # Создаем основное окно
        self.root = tkinter.Tk()
        self.root.title("Messenger")

        self.api = API()

        # Создаем меню
        #self.menu()

        # Создаем фрейм со списком контактов
        self.contact_frame()

        # Создаем фрейм с чатом
        self.message_frame()

        # Выводим основное окно
        self.root.mainloop()

    def send_message(self, event):
        '''
        Метод для отправки сообщения
        '''

        message = self.send_message_text.get("1.0", tkinter.END)
        self.api.send_message(message)
        self.get_chat(event)

    def get_chat(self, event):
        contact = self.contact_listbox.get(self.contact_listbox.curselection())
        msgs = self.api.get_contact(contact)
        self.chat_text.destroy()
        self.chat_text = tkinter.Text(self.chat_frame, width=50, height=15, font="Arial 9")
        txt_msg = self.parse_chat(msgs)
        self.chat_text.insert(tkinter.CURRENT, txt_msg)
        self.chat_text.config(state=tkinter.DISABLED)
        self.chat_text.yview(tkinter.END)
        self.chat_text.pack(expand=1, fill=tkinter.BOTH)


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
            text_chat = text_chat + message[0] + ' : ' + message[1] + '\n'
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

        msgs = self.api.get_chat()

        self.chat_text = tkinter.Text(self.chat_frame, width=50, height=15, font="Arial 9")
        txt_msg = self.parse_chat(msgs)
        self.chat_text.insert(tkinter.CURRENT, txt_msg)
        self.chat_text.config(state=tkinter.DISABLED)
        self.chat_text.yview(tkinter.END)
        self.chat_text.pack(expand=1, fill=tkinter.BOTH)

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

    #def menu(self):
    #    self.main_menu = tkinter.Menu(self.root)
    #    self.root.config(menu=self.main_menu)

    #    fm = tkinter.Menu(self.main_menu) # создается пункт меню с размещением на основном меню (m)
    #    self.main_menu.add_cascade(label="File",menu=fm) #пункту располагается на основном меню (m)
    #    fm.add_command(label="Open...") #формируется список команд пункта меню
    #    fm.add_command(label="New")
    #    fm.add_command(label="Save...")
    #    fm.add_command(label="Exit")

    #    hm = tkinter.Menu(self.main_menu) #второй пункт меню
    #    self.main_menu.add_cascade(label="Help",menu=hm)
    #    hm.add_command(label="Help")
    #    hm.add_command(label="About")


