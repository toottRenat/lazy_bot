from tkinter.filedialog import *
import tkinter.messagebox
import tkinter
import subprocess


def add_to_path(op):
    s = ''
    i = -5
    while op[i] != '/':
        s += op[i]
        i -= 1
    s = s[::-1]
    #print(s)
    #print(op[:i])
    subprocess.run(["setx", 'path', '"%path%;{0}"'.format(op[:i])], shell=True)


class PathAdder(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)

        self.var = StringVar()
        self.description = Message(self, textvariable=self.var, width=400)
        self.description.grid(row=0, column=1)
        self.var.set('Выберете исполняемый файл для добавления его в PATH')

        self.mainloop()

    def open_file(self):  # выбор файла для обработки
        op = askopenfilename()
        if len(op) == 0:  # если просто закрыли окно выбора
            pass
        elif op[-1:-5:-1][::-1] != '.exe':  # если выбрали не *.exe файл
            tkinter.messagebox.showerror('Wrong type of file',
                                         "Файл должен иметь расширение *.exe, выберете корректный файл")
            self.open_file()
        else:  # если все в порядке
            add_to_path(op)
            tkinter.messagebox.showinfo("Info", 'Файл, раположеный по пути "{0}" был успешно добавлен в PATH'.format(op))

if __name__ == '__main__':
    pa = PathAdder()
