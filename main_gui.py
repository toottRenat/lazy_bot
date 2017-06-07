from multiprocessing import Process

from lib.gui import path_adder, demon_settings
import demon


if __name__ == '__main__':
    processes = []
    processes.append(Process(target=demon_settings.pseudo_main))
    processes.append(Process(target=demon.pseudo_main))
    for p in processes:
        p.start()
