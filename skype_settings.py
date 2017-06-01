import tkinter.messagebox
from lib.lazy_tkinter import MyEntry, MyButton, MyLabel
from tkinter import *


class SkypeConfig(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.id_label = MyLabel(self, 0, 0, "Никнейм или номер телефона контакта:")
        self.id_entry = MyEntry(self, 0, 1)

        self.name_label = MyLabel(self, 1, 0, "Слово, соответствующее вызову данного контакта:")
        self.name_entry = MyEntry(self, 1, 1)

        self.accept_button = MyButton(self, 'Запомнить', 2, 1, cur_func=self.add_contact)

        self.mainloop()

    def add_contact(self, event):  # возможно, стоит также сделать возможность удалять и просматривать эти строки
        if self.name_entry.get() != '' and self.id_entry.get() != '':
            with open('var/skype/contacts.txt', 'a') as f:
                f.write(' : '.join([self.name_entry.get(), self.id_entry.get()]))
                f.write('\n')
                tkinter.messagebox.showinfo('Well done', "Контакт успешно добавлен")
        else:
            tkinter.messagebox.showerror('Error', "Необходимо заполнить все поля!")

if __name__ == '__main__':
    pa = SkypeConfig()
