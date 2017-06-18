import pyaudio
import wave
from tkinter.filedialog import *

from lib.lazy_tkinter import MyButton, MyMessage


CHUNK = 1024


class Player:
    pause_flag = True

    def __init__(self, root):

        self.var = StringVar()
        self.current_song = Message(root, textvariable=self.var, width=100)
        self.current_song.grid(row=0, column=1)
        self.var.set('')

        self.message = MyMessage(root, 'Current song:', 0, 0, my_width=80, my_relief='flat')

        self.start_button = MyButton(root, 1, 2, cur_func=self.start_playing, my_color="blue", my_text="Start")
        self.stop_button = MyButton(root, 1, 1, cur_func=self.start_playing, my_color="red", my_text="Stop")

    def callback(self, in_data, frame_count, time_info, status):

        return in_data, pyaudio.paContinue

    def pause_or_resume(self, _):
        if self.pause_flag:
            self.stream.start_stream()
            self.pause_or_not()
        else:
            try:
                self.stream.stop_stream()
            except OSError:
                self.stream = self.p.open(format=self.p.get_format_from_width(self.sample_width),
                                          channels=2,
                                          rate=self.frame_rate,
                                          output=True,
                                          frames_per_buffer=CHUNK,
                                          stream_callback=self.callback)
                #self.stream.stop_stream()
            self.pause_or_not()

    def start_playing(self, _):  # начало воспроизведения
        self.var.set('365days.wav')
        self.wf = wave.open(self.var.get(), 'rb')
        self.p = pyaudio.PyAudio()
        self.frame_rate = self.wf.getframerate()
        self.sample_width = self.wf.getsampwidth()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.sample_width),
                                  channels=2,
                                  rate=self.frame_rate,
                                  output=True,
                                  frames_per_buffer=CHUNK,
                                  stream_callback=self.callback)

    def stop_playing(self, _):  # остановить воспроизведение текущей композиции
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            self.start_button = MyButton(self, "Start", 3, 5, cur_func=self.start_playing, my_bg="blue")
            self.processed_buffer = b''
            if self.pause_flag:
                self.pause_or_not()
        except AttributeError:
            pass

    def pause_or_not(self):  # в зависимости от метки меняет метку и кнопку
        if self.pause_flag:
            self.start_button = MyButton(root, 1, 2, cur_func=self.start_playing, my_color="blue", my_text="Stop")
            self.pause_flag = False
        else:
            self.start_button = MyButton(root, 1, 2, cur_func=self.start_playing, my_color="blue", my_text="Start")
            self.pause_flag = True

if __name__ == '__main__':
    root = Tk()
    p = Player(root)
    root.mainloop()
