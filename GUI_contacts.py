import tkinter
import tkinter.messagebox

class GUI_contacts:

    # TODO при закрытии окна перезагружать основное окно мессенджера

    def __init__(self, gui):

        self.gui = gui

        self.contact_win = tkinter.Toplevel(self.gui.root)
        self.contact_win.title('Контакты')

        # фиксированный размер окна
        self.contact_win.minsize(width=400,height=200)
        self.contact_win.maxsize(width=400,height=200)

        # Создаем меню
        self.menu()

        self.contact_frame()

    def menu(self):
        self.tool_bar = tkinter.Menu(self.contact_win)
        self.contact_win.config(menu=self.tool_bar)
        self.tool_bar.add_command(label='\u002B', command=self.add_contact)

    def contact_frame(self, reload_frame = False):
        '''
        Метод для отображения списка контактов
        '''

        # TODO если выбрать контакт в главном окне мессенджера,
        # а потом вызвать окно контактов (это окно) и в нем выбрать этот же контакт возникает Exception in Tkinter callback
        # возможно связано с тем что этот класс использует обьект класса GUI

        if (reload_frame):
            self.contacts_frame.destroy()
            self.contacts_info_frame.destroy()

        # Создаем фрейм для списка контактов
        self.contacts_frame = tkinter.Frame(self.contact_win)
        self.contacts_frame.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # Создаем и выводим список контактов
        contact_list = self.gui.api.get_contact_list()
        self.contacts_listbox = tkinter.Listbox(self.contacts_frame, selectmode=tkinter.SINGLE, height=6)
        for contact in contact_list:
            self.contacts_listbox.insert(tkinter.END, contact)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.get_contact_info)
        self.contacts_listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

        # Создаем пустой фрейм для информации о контакте
        self.contacts_info_frame = tkinter.Frame(self.contact_win)
        self.contacts_info_frame.pack()


    def get_contact_info(self, event):
        '''
        Получение информации о контакте
        '''

        contact = self.contacts_listbox.get(self.contacts_listbox.curselection())
        # удаление online/offline из имени контакта
        contact = self.gui.del_online_offline_simbol(contact)

        self.contact = self.gui.model.get_contact(contact)

        self.contact_info_frame()

    def contact_info_frame(self, edit = True):
        '''
        Метод для создания фрейма просмотра, редактирования и удаления информации о контакте

        если edit = True значит мы редактируем запись из базы, а если False значит создаем новую
        '''

        self.contacts_info_frame.destroy()

        # Создаем фрейм для информации о контакте
        self.contacts_info_frame = tkinter.Frame(self.contact_win)
        self.contacts_info_frame.pack(expand=1)

        # Поле ввода имени контакта
        self.contact_name_frame = tkinter.Frame(self.contacts_info_frame)
        self.contact_name_frame.pack()

        self.contact_name_lable = tkinter.Label(self.contact_name_frame, text="Имя", font="Arial 9")
        self.contact_name_lable.pack()

        self.contact_name_entry = tkinter.Entry(self.contact_name_frame, width=30, font="Arial 9")
        if (edit):
            self.contact_name_entry.insert(0, self.contact[1])
        self.contact_name_entry.pack()

        # Поле ввода ключа контакта
        self.contact_key_frame = tkinter.Frame(self.contacts_info_frame)
        self.contact_key_frame.pack()

        self.contact_key_lable = tkinter.Label(self.contact_key_frame, text="Ключ", font="Arial 9")
        self.contact_key_lable.pack()

        self.contact_key_entry = tkinter.Text(self.contact_key_frame, width=30, height=5, font="Arial 9")
        if (edit):
            self.contact_key_entry.insert(tkinter.CURRENT, self.contact[2])
        self.contact_key_entry.pack()

        # Кнопки сохранить и удалить
        self.contact_button_frame = tkinter.Frame(self.contacts_info_frame)
        self.contact_button_frame.pack()

        self.contact_save_button = tkinter.Button(self.contact_button_frame, text='\u2713', font="Arial 9")
        if (edit):
            self.contact_save_button.bind("<Button-1>", self.save_contact)
        else:
            self.contact_save_button.bind("<Button-1>", self.save_new_contact)
        self.contact_save_button.pack(side=tkinter.LEFT)

        if (edit):
            self.contact_save_button = tkinter.Button(self.contact_button_frame, text='\u2715', font="Arial 9")
            self.contact_save_button.bind("<Button-1>", self.del_contact)
            self.contact_save_button.pack(side=tkinter.LEFT)

    def save_new_contact(self, event):

        name = self.contact_name_entry.get()
        key  = self.contact_key_entry.get("1.0", tkinter.END)

        self.gui.model.add_contact(name, key)

        self.contact_frame(True)

    def save_contact(self, event):
        print('save')

    def del_contact(self, event):
        print('del')

    def add_contact(self):
        self.contact_info_frame(False)

