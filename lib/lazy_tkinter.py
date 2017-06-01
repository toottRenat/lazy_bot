from tkinter import *


def pass_f(event):
    pass


class MyButton:
    def __init__(self, root, my_text, my_row, my_column, cur_func=pass_f, my_state='normal'):
        self.button = Button(root,
                             text=my_text, font='Arial 10',
                             width=10, height=3,
                             bg="white", fg="black",
                             state=my_state)
        self.button.grid(row=my_row, column=my_column)
        self.button.bind("<Button-1>", cur_func)  # при нажатии ЛКМ на кнопку вызывается функция cur_func

    def config(self, my_state="normal"):
        self.button.config(state=my_state)


class MyCheckButton:
    def __init__(self, root, my_text, my_row, my_column, my_var):
        self.check_button = Checkbutton(root, text=my_text, variable=my_var, onvalue=1, offvalue=0, height=5, width=20)
        self.check_button.grid(row=my_row, column=my_column)


class MyScale:
    def __init__(self, root, my_row, my_column, start, end, my_from=5, my_to=0, my_resolution=0.1):
        self.scale = Scale(root,
                           length=300,
                           from_=my_from, to=my_to,
                           resolution=my_resolution)
        self.scale.grid(row=my_row, column=my_column)
        self.scale.set(1)
        self.start = start
        self.lf = []
        self.rf = []
        self.end = end

    def get_value(self):
        return float(self.scale.get())

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class MyMessage:
    def __init__(self, root, message, my_row, my_column, my_width=90, my_relief='raised'):
        self.var = StringVar()
        self.message = Message(root,
                               width=my_width,
                               textvariable=self.var,
                               relief=my_relief)
        self.message.grid(row=my_row, column=my_column)
        self.var.set(message)


class MyEntry:
    def __init__(self, root, my_row, my_column, my_width=30, my_relief='raised'):
        self.entry = Entry(root,
                           width=my_width,
                           relief=my_relief)
        self.entry.grid(row=my_row, column=my_column)

    def get(self):
        return self.entry.get()


class MyLabel:
    def __init__(self, root, my_row, my_column, text):
        self.id_label = Label(root, text=text)
        self.id_label.grid(row=my_row, column=my_column)
