import tkinter.messagebox
import demon
from lib.lazy_tkinter import MyEntry, MyButton, MyLabel
#from lazy_bot import demon
#from lazy_bot.lib.lazy_tkinter import MyEntry, MyButton, MyLabel
import PIL.Image
import PIL.ImageTk
from functools import partial
from tkinter.filedialog import *


PREFIX = ''


class SkypeConfig:
    def __init__(self, root):
        self.root = root
        self.root["bg"] = "azure"
        self.top = Toplevel()
        self.top.protocol("WM_DELETE_WINDOW", self.__top_die)

        self.top.withdraw()
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Показать все контакты", command=self.show_content)
        self.menubar.add_cascade(label="Редактировать", menu=self.filemenu)
        root.config(menu=self.menubar)

        self.id_label = MyLabel(root, 0, 0, "Никнейм или номер телефона контакта:", my_color='azure')
        self.id_entry = MyEntry(root, 0, 1, my_color='lemon chiffon')

        self.name_label = MyLabel(root, 1, 0, "Слово, соответствующее вызову данного контакта:", my_color='azure')
        self.name_entry = MyEntry(root, 1, 1, my_color='lemon chiffon')

        self.accept_button = MyButton(root, 2, 1, my_text='Запомнить',
                                      cur_func=self.add_contact,
                                      my_color='lemon chiffon')  # скорее всего можно найти и получше цвет для кнопок

        self.voice_button = MyButton(root,  2, 0,my_text='Использовать голос',
                                     cur_func=self.get_from_micro, my_width=20,
                                     my_color='lemon chiffon')

    def add_contact(self, _):  # возможно, стоит также сделать возможность удалять и просматривать эти строки
        if self.name_entry.get() != '' and self.id_entry.get() != '':
            with open('../../var/skype/contacts.txt', 'a') as f:
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

    def show_content(self):
        self.top.deiconify()
        self.top["bg"] = "azure"
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        with open(''.join([PREFIX, 'var/skype/contacts.txt']), 'r') as f:
            for line in f:
                label = MyLabel(self.top, i, 0, line,
                                my_color='azure')
                button = Button(self.top, font='Arial 10',
                                width=30, height=25,
                                fg="black", state='normal')
                button.grid(row=i, column=1)
                button.bind("<Button-1>", partial(self.delete_line, i))
                button["image"] = img
                button["compound"] = CENTER
                i += 1
        self.top.mainloop()

    def delete_line(self, i, _):
        st = ''
        print(i)
        with open(''.join([PREFIX, 'var/skype/contacts.txt']), 'r') as f:
            for j, line in enumerate(f):
                if j != i:
                    st = ''.join([st, line])
        with open(''.join([PREFIX, 'var/skype/contacts.txt']), 'w') as f:
            f.write(st)
        self.__refresh()

    def __refresh(self):
        for w in self.top.winfo_children():
            w.destroy()
        self.top.withdraw()
        self.show_content()

    def __top_die(self):
        self.top.withdraw()


def pseudo_main():
    root = Tk()
    root.geometry("500x200+10+10")
    root.title("Demon gui")
    #root.resizable(False, False)
    pa = SkypeConfig(root)
    root.mainloop()

if __name__ == '__main__':
    PREFIX = '../../'
    pseudo_main()
