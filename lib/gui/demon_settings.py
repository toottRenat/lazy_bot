import tkinter.messagebox
import demon
from lib.lazy_tkinter import MyEntry, MyButton, MyLabel
import PIL.Image
import PIL.ImageTk
from functools import partial
from tkinter.filedialog import *


PREFIX = ''


class DemonConfig:
    def __init__(self, root):
        self.root = root
        self.root["bg"] = "azure"
        #self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw())
        self.__show_menu()

    def __show_menu(self):
        self.menubar = Menu(self.root)

        self.config_menu = Menu(self.menubar, tearoff=0)
        self.config_menu.add_command(label="Запуск программы", command=self.start_config)  # todo
        self.config_menu.add_command(label="Поиск в интернете", command=self.add_skype)  # todo
        self.config_menu.add_command(label="Запись", command=self.add_skype)  # todo
        self.config_menu.add_command(label="Звонок по Skype", command=self.add_skype)  # todo
        self.menubar.add_cascade(label="Команды помощника", menu=self.config_menu)

        self.skype_menu = Menu(self.menubar, tearoff=0)
        self.skype_menu.add_command(label="Удалить контакты", command=self.change_skype)
        self.skype_menu.add_command(label="Добавить контакты", command=self.add_skype)
        self.menubar.add_cascade(label="Skype", menu=self.skype_menu)

        self.root.config(menu=self.menubar)

    def add_skype(self):
        self.__die_root()
        self.id_label = MyLabel(self.root, 0, 0, "Никнейм или номер телефона контакта:", my_color='azure')
        self.id_entry = MyEntry(self.root, 0, 1, my_color='lemon chiffon')

        self.name_label = MyLabel(self.root, 1, 0, "Слово, соответствующее вызову данного контакта:", my_color='azure')
        self.name_entry = MyEntry(self.root, 1, 1, my_color='lemon chiffon')

        self.accept_button = MyButton(self.root, 2, 1, my_text='Запомнить',
                                      cur_func=self.add_contact,
                                      my_color='lemon chiffon')  # скорее всего можно найти и получше цвет для кнопок

        self.voice_button = MyButton(self.root,  2, 0, my_text='Использовать голос',
                                     cur_func=self.get_from_micro, my_width=20,
                                     my_color='lemon chiffon')

    def add_contact(self, _):  # возможно, стоит также сделать возможность удалять и просматривать эти строки
        if self.name_entry.get() != '' and self.id_entry.get() != '':
            with open(''.join([PREFIX, 'var/skype/contacts.txt']), 'a') as f:
                f.write(' : '.join([self.name_entry.get(), self.id_entry.get()]))
                f.write('\n')
                tkinter.messagebox.showinfo('Well done', "Контакт успешно добавлен")
        else:
            tkinter.messagebox.showerror('Error', "Необходимо заполнить все поля!")

    def get_from_micro(self, _):
        demon.tell_and_die(speech='Как запомнить данный контакт?')
        while True:
            st = demon.get_word()
            if st != '':
                self.name_entry.insert(0, st)
                break

    def change_skype(self):  # картинка не показывается wtf
        st_file = ''.join([PREFIX, 'var/skype/contacts.txt'])
        self.__die_root()
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))  # wtf
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        with open(st_file, 'r') as f:
            for line in f:
                label = MyLabel(self.root, i, 0, line,
                                my_color='azure')
                button = Button(self.root, width=30,
                                height=25, state='normal')
                button.grid(row=i, column=1)
                button.bind("<Button-1>", partial(self.__delete_line, i, st_file, self.change_skype))
                button["image"] = img
                button["compound"] = CENTER
                i += 1

    def start_config(self):
        st_file = ''.join([PREFIX, 'var/conf/start_config.txt'])
        self.__die_root()
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))  # мб разные надо
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        with open(st_file, 'r') as f:
            for line in f:
                label = MyLabel(self.root, i, 0, line,
                                my_color='azure')
                button = Button(self.root, width=30,
                                height=25, state='normal')
                button.grid(row=i, column=1)
                button.bind("<Button-1>", partial(self.__delete_line, i, st_file, self.start_config))
                button["image"] = img
                button["compound"] = CENTER
                i += 1

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
    PREFIX = '../../'
    pseudo_main()
