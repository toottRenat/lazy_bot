
"""
Мб нужна документация на эту прогу, но так лень...
По идее все просто пока...
"""

import tkinter.messagebox
import demon
from lib.lazy_tkinter import MyEntry, MyButton, MyLabel
#from lazy_bot import demon
#from lazy_bot.lib.lazy_tkinter import MyEntry, MyButton, MyLabel
import PIL.Image
import PIL.ImageTk
from functools import partial  # детка избавляет от сотен строк кода, лайк, репост
from tkinter.filedialog import *


PREFIX = ''


class DemonConfig:
    start_conf_file = ''.join([PREFIX, 'var/conf/start_config.txt'])
    search_conf_file = ''.join([PREFIX, 'var/conf/search_config.txt'])
    record_conf_file = ''.join([PREFIX, 'var/conf/record_config.txt'])
    skype_call_conf_file = ''.join([PREFIX, 'var/conf/skype_call_config.txt'])

    skype_contacts_file = ''.join([PREFIX, 'var/skype/contacts.txt'])
    skype_conf_file = ''.join([PREFIX, 'var/conf/skype_config.txt'])

    def __init__(self, root):
        self.root = root
        self.root["bg"] = "azure"
        self.__show_menu()

    def __show_menu(self):
        self.menubar = Menu(self.root)

        self.config_menu = Menu(self.menubar, tearoff=0)
        self.config_menu.add_command(label="Запуск программы",
                                     command=partial(self.any_config, self.start_conf_file, self.any_config))
        self.config_menu.add_command(label="Поиск в интернете",
                                     command=partial(self.any_config, self.search_conf_file, self.any_config))
        self.config_menu.add_command(label="Запись",
                                     command=partial(self.any_config, self.record_conf_file, self.any_config))
        self.config_menu.add_command(label="Звонок по Skype",
                                     command=partial(self.any_config, self.skype_call_conf_file, self.any_config))
        self.menubar.add_cascade(label="Команды помощника", menu=self.config_menu)

        self.skype_menu = Menu(self.menubar, tearoff=0)
        self.skype_menu.add_command(label="Удалить контакты", command=self.change_skype)
        self.skype_menu.add_command(label="Добавить контакты", command=self.add_skype)
        self.menubar.add_cascade(label="Skype", menu=self.skype_menu)

        self.root.config(menu=self.menubar)

    def add_skype(self):
        self.__die_root()
        entries = []
        id_label = MyLabel(self.root, 0, 0, "Никнейм или номер телефона контакта:", my_color='azure')
        entries.append(MyEntry(self.root, 0, 1, my_color='lemon chiffon'))

        name_label = MyLabel(self.root, 1, 0, "Слово, соответствующее вызову данного контакта:", my_color='azure')
        entries.append(MyEntry(self.root, 1, 1, my_color='lemon chiffon'))

        accept_button = MyButton(self.root, 2, 1, my_text='Запомнить',
                                 cur_func=partial(self.add_content, entries,
                                                  self.skype_contacts_file, ' : ', self.add_skype),
                                 my_color='lemon chiffon')  # скорее всего можно найти и получше цвет для кнопок

        voice_button = MyButton(self.root,  2, 0, my_text='Использовать голос',
                                cur_func=self.get_from_micro, my_width=20,
                                my_color='lemon chiffon')

    @staticmethod
    def add_content(entries, file, joining, refresh, _):
        if '' not in [i.get() for i in entries]:
            with open(file, 'a') as f:
                f.write(joining.join([i.get() for i in entries]))
                f.write('\n')
                tkinter.messagebox.showinfo('Well done', "Данные успешно добавлены")
        else:
            tkinter.messagebox.showerror('Error', "Необходимо заполнить все поля!")
        refresh(file, refresh)

    def get_from_micro(self, _):
        demon.tell_and_die(speech='Как запомнить данный контакт?')
        while True:
            st = demon.get_word()
            if st != '':
                self.name_entry.insert(0, st)
                break

    def change_skype(self):  # было бы круто подогнать это под any_config
        # картинка не показывается wtf
        self.__die_root()
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))  # wtf
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        with open(self.skype_contacts_file, 'r') as f:
            for line in f:
                label = MyLabel(self.root, i, 0, line,
                                my_color='azure')
                button = Button(self.root, width=30,
                                height=25, state='normal')
                button.grid(row=i, column=1)
                button.bind("<Button-1>", partial(self.__delete_line, i, self.skype_contacts_file, self.change_skype))
                button["image"] = img
                button["compound"] = CENTER
                i += 1

    def any_config(self, file, refresh):
        self.__die_root()
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))  # мб разные надо
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        with open(file, 'r') as f:
            for line in f:
                label = MyLabel(self.root, i + 3, 0, line,
                                my_color='azure')
                button = Button(self.root, width=30,
                                height=25, state='normal')
                button.grid(row=i + 3, column=1)
                button.bind("<Button-1>", partial(self.__delete_line, i, file,
                                                  partial(self.any_config, self.start_conf_file, self.any_config)))
                button["image"] = img
                button["compound"] = CENTER
                i += 1

        entry = MyEntry(self.root, 0, 0, my_color='lemon chiffon')

        accept_button = MyButton(self.root, 2, 1, my_text='Запомнить',
                                 cur_func=partial(self.add_content, [entry],
                                                  file, '', refresh),
                                 my_color='lemon chiffon')  # скорее всего можно найти и получше цвет для кнопок

        voice_button = MyButton(self.root,  2, 0, my_text='Использовать голос',
                                cur_func=self.get_from_micro, my_width=20,
                                my_color='lemon chiffon')

    @staticmethod
    def __delete_line(i, file, caller, _):
        st = ''
        with open(file, 'r') as f:
            for j, line in enumerate(f):
                if j != i:
                    st = ''.join([st, line])
        with open(file, 'w') as f:
            f.write(st)
        caller()

    def __die_root(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.__show_menu()


def pseudo_main():
    root = Tk()
    root.geometry("500x200+10+10")
    root.title("Demon gui")
    #root.resizable(False, False)
    pa = DemonConfig(root)
    root.mainloop()

if __name__ == '__main__':
    #PREFIX = '../../'
    pseudo_main()
