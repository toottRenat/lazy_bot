
"""
Мб нужна документация на эту прогу, но так лень...
По идее все просто пока...
Мб стоит что-то расписать перед поездкой на сборы
"""

import demon
from lib.lazy_tkinter import MyEntry, MyButton, MyLabel
import tkinter.messagebox

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
    youtube_conf_file = ''.join([PREFIX, 'var/conf/youtube_config.txt'])
    vk_message_conf_file = ''.join([PREFIX, 'var/conf/vk_message_config.txt'])
    vk_conf_file = ''.join([PREFIX, 'var/conf/vk_config.txt'])
    play_music_file = ''.join([PREFIX, 'var/conf/play_music_config.txt'])

    def __init__(self, root):
        self.root = root
        self.root["bg"] = "azure"
        self.__show_menu()

    def __show_menu(self):
        self.menubar = Menu(self.root)

        st = 'Назовите команду, которая будет'

        self.config_menu = Menu(self.menubar, tearoff=0)
        self.config_menu.add_command(label="Запуск программы",
                                     command=partial(self.any_config, self.start_conf_file,
                                                     self.any_config, ' '.join([st, 'запускать программы']),
                                                     1, ['Команда, после которой будет запуск программы:']))
        self.config_menu.add_command(label="Поиск в интернете",
                                     command=partial(self.any_config, self.search_conf_file,
                                                     self.any_config, ' '.join([st, 'искать в интернете']),
                                                     1, ['Команда, после которой будет поиск в интернете:']))
        self.config_menu.add_command(label="Запись",
                                     command=partial(self.any_config, self.record_conf_file,
                                                     self.any_config, ' '.join([st, 'записывать в файл']),
                                                     1, ['Команда, после которой будет запись в файл:']))
        self.config_menu.add_command(label="Видео в Youtube",
                                     command=partial(self.any_config, self.youtube_conf_file,
                                                     self.any_config, ' '.join([st, 'искать видео']),
                                                     1, ['Команда, после которой будет поиск в YouTube:']))
        # нужно додумать, т.к. с колонками он будет все пытаться распознать
        self.config_menu.add_command(label="Музыка(локально)",  # todo
                                     command=partial(self.any_config, self.play_music_file,
                                                     self.any_config, ' '.join([st, 'воспроизводить музыку']),
                                                     1, ['Команда, после которой будет запуск музыки:']))
        self.menubar.add_cascade(label="Команды помощника", menu=self.config_menu)

        self.skype_menu = Menu(self.menubar, tearoff=0)
        self.skype_menu.add_command(label="Звонок по Skype",
                                    command=partial(self.any_config, self.skype_call_conf_file,
                                                    self.any_config, ' '.join([st, 'звонить по Skype']),
                                                    1, ['Команда, после которой будет звонок по Skype:']))
        self.skype_menu.add_command(label="Изменить контакты",
                                    command=partial(self.any_config, self.skype_contacts_file,
                                                    self.any_config, 'Назовите контакт Skype',
                                                    2, ['Никнейм или номер телефона контакта:',
                                                        "Слово, соответствующее данному контакту:"]))
        self.menubar.add_cascade(label="Skype", menu=self.skype_menu)

        self.vk_menu = Menu(self.menubar, tearoff=0)
        self.vk_menu.add_command(label="Написать сообщение",
                                 command=partial(self.any_config, self.vk_conf_file,
                                                 self.any_config, ' '.join([st, 'написать в Vkontakte']),
                                                 1, ['Команда, после которой будет сообщение через Vkontakte:']))
        self.vk_menu.add_command(label="Изменить контакты",
                                 command=partial(self.any_config, self.vk_message_conf_file,
                                                 self.any_config, 'Назовите контакт Vkontakte',
                                                 2, ["Слово, соответствующее данному контакту:",
                                                     'ID контакта:']))

        self.menubar.add_cascade(label="Vkontakte", menu=self.vk_menu)

        self.root.config(menu=self.menubar)

    @staticmethod
    def add_content(entries, file, joining, refresh, speech, labels, _):
        if '' not in [i.get() for i in entries]:
            with open(file, 'a') as f:
                f.write(joining.join([i.get().lower() for i in entries]))
                f.write('\n')
                tkinter.messagebox.showinfo('Well done', "Данные успешно добавлены")
        else:
            tkinter.messagebox.showerror('Error', "Необходимо заполнить все поля!")
        refresh(file, refresh, speech, len(entries), labels)

    @staticmethod
    def get_from_micro(entry, speech, _):
        demon.tell_and_die(speech=speech)
        while True:
            st = demon.get_word()
            if st != '':
                entry[-1].insert(0, st)
                break

    def any_config(self, file, refresh, speech, n_entries, labels):
        joining = {1: '', 2: ' : '}
        self.__die_root()
        src_image = PIL.Image.open(''.join([PREFIX, 'share/button_images/Cross_30x25.jpg']))
        img = PIL.ImageTk.PhotoImage(src_image)
        i = 0
        try:
            f = open(file, 'r')
            f.close()
        except FileNotFoundError:
            f = open(file, 'w')
            f.close()
        with open(file, 'r') as f:
            for line in f:
                label = MyLabel(self.root, i + 4, 0, line,
                                my_color='azure')
                button = Button(self.root, width=30,
                                height=25, state='normal')
                button.grid(row=i + 4, column=1)
                button.bind("<Button-1>", partial(self.__delete_line, i, file,
                                                  partial(self.any_config, file,
                                                          self.any_config, speech,
                                                          n_entries, labels)))
                button["image"] = img
                button["compound"] = CENTER
                i += 1
        j = 0
        entries = []
        while j < n_entries:
            label = MyLabel(self.root, j, 0, labels[j], my_color='azure')
            entries.append(MyEntry(self.root, j, 1, my_color='lemon chiffon'))  # можно b2ec5d
            j += 1
        accept_button = MyButton(self.root, j + 1, 1, my_text='Запомнить',
                                 cur_func=partial(self.add_content, entries,
                                                  file, joining[n_entries], refresh, speech, labels),
                                 my_color='lemon chiffon')  # скорее всего можно найти и получше цвет для кнопок

        voice_button = MyButton(self.root, j + 1, 0, my_text='Использовать голос',
                                cur_func=partial(self.get_from_micro, entries, speech), my_width=20,
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
    root.geometry("600x500+10+10")
    root.title("Demon gui")
    #root.resizable(False, False)
    pa = DemonConfig(root)
    root.mainloop()

if __name__ == '__main__':
    #PREFIX = '../../'
    pseudo_main()
