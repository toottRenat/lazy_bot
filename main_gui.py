from tkinter.filedialog import *
import tkinter.messagebox
import tkinter
from multiprocessing import Process

from lib.gui import path_adder, skype_settings
from lib import lazy_tkinter
import demon


class FirstAppearance:
    def __init__(self, root):
        root["bg"] = "azure"

if __name__ == '__main__':
    processes = []
    processes.append(Process(target=skype_settings.pseudo_main))
    processes.append(Process(target=demon.pseudo_main))
    for p in processes:
        p.start()
