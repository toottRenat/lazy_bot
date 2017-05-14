#!/usr/bin/env python
# -*- coding: utf-8 -*-

import speech_recognition as sr
import subprocess
import webbrowser
import pyglet
import os
import time
from gtts import gTTS


def tell_and_die(speech='', name='1.mp3'):
    if name == '1.mp3':
        tts = gTTS(text=speech, lang='ru')
        tts.save("1.mp3")
        sound = pyglet.resource.media('1.mp3', streaming=False)
        sound.play()
        os.remove('1.mp3')
    else:
        sound = pyglet.resource.media(name, streaming=False)
        sound.play()


def get_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-нибудь")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    s = ''
    try:
        s = r.recognize_google(audio, language="ru-RU")
        print(s)
    except sr.UnknownValueError:
        print("Робот не расслышал фразу")
    except sr.RequestError as e:
        print("Ошибка сервиса; {0}".format(e))
    return s


def ggl():
    tell_and_die(speech='Что найти?')
    while True:
        new_st = get_word()
        if new_st != '':
            break
    tell_and_die(name='recorded_sounds/sklonyayus-pered-vashej-volej.mp3')
    webbrowser.open('https://www.google.ru/search?q={0}&oq={1}&aqs=chrome.0.69i59j69i61.'
                    '775j0j8&sourceid=chrome&ie=UTF-8'.format(new_st, new_st))


def start():
    tell_and_die(speech='Какую программу запустить?')
    while True:
        new_st = get_word()
        if new_st != '':
            break
    try:
        #p = subprocess.check_call(' '.join(['start', new_st]), shell=True)
        #print('out:', p)
        with subprocess.Popen(' '.join(['start', new_st]), shell=True) as p:
            time.sleep(1)
            p.terminate()
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))


def record():  # todo
    tell_and_die(speech='В какой файл записать?')

    while True:
        print('Скажите название файла')
        new_st = get_word()
        if new_st != '':
            break
    try:
        file = open(''.join([new_st, '.txt']))
    except IOError as e:
        open_and_write(new_st)
    else:
        file.close()
        open_and_write(new_st, mode='a')


def open_and_write(file_name, mode='w'):
    with open(''.join([file_name, '.txt']), mode) as file:
        tell_and_die(speech='Запись началась')
        while True:
            new_st = get_word()
            if new_st.lower() == 'закончить запись' or new_st.lower() == 'закончи запись':
                break
            else:
                if new_st != '':
                    file.write(new_st + '\n')
                    tell_and_die(speech='Продолжайте')
        tell_and_die(speech='Запись успешно завершена')
        file.write('\n')


if __name__ == '__main__':
    while True:
        st = get_word().lower()
        if st == 'поиск':
            ggl()
        elif st == 'запуск':
            start()
        elif st == 'запись':
            record()
