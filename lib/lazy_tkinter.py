from tkinter import *


"""
Все должно быть ясно и без документации, либа детская.
Онли классы-хелперы.
"""


def pass_f(_):
    pass


class MyButton(Button):
    def __init__(self, root, my_row, my_column, cur_func=pass_f, my_text=None,
                 my_state='normal', my_width=10, my_color='white', my_height=3, img=None, command=None):
        super(MyButton, self).__init__(root, font='Arial 10',
                                       width=my_width, height=my_height,
                                       bg=my_color, fg="black",
                                       state=my_state, command=command)
        self.grid(row=my_row, column=my_column)
        self.bind("<Button-1>", cur_func)
        if my_text is None:
            self["image"] = img
            self["compound"] = CENTER
        else:
            self["text"] = my_text


class MyCheckButton(Checkbutton):
    def __init__(self, root, my_text, my_row, my_column, my_var):
        super(MyCheckButton, self).__init__(root, text=my_text, variable=my_var,
                                            onvalue=1, offvalue=0, height=5, width=20)
        self.grid(row=my_row, column=my_column)


class MyScale(Scale):  # пока не используется, так что может потребоваться доработка
    def __init__(self, root, my_row, my_column, start, end, my_from=5, my_to=0, my_resolution=0.1):
        super(MyScale, self).__init__(root, length=300,
                                      from_=my_from, to=my_to,
                                      resolution=my_resolution)
        self.grid(row=my_row, column=my_column)
        self.set(1)
        self.start = start
        self.lf = []
        self.rf = []
        self.end = end


class MyMessage(Message):
    def __init__(self, root, message, my_row, my_column, my_width=90, my_relief='raised'):
        super(MyMessage, self).__init__(root, width=my_width,
                                        textvariable=self.var,
                                        relief=my_relief)
        self.var = StringVar()
        self.grid(row=my_row, column=my_column)
        self.var.set(message)


class MyEntry(Entry):
    def __init__(self, root, my_row, my_column, my_width=30, my_relief='raised', my_color='white'):
        super(MyEntry, self).__init__(root, width=my_width,
                                      relief=my_relief, bg=my_color)
        self.grid(row=my_row, column=my_column)


class MyLabel(Label):
    def __init__(self, root, my_row, my_column, text, my_color='white'):
        super(MyLabel, self).__init__(root, text=text, bg=my_color)
        self.grid(row=my_row, column=my_column)
