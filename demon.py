# -*- encoding: utf-8 -*-
# !/usr/bin/env python3
"""
Simple speech recognition program.

It provides different opportunities like googling,
recording,  starting another programs, calling with Skype.

Available functions:
- tell_and_die: Tells given sentence or plays given recorded sound using pyglet.
- get_word: Waiting until something meaningful will be told and returns it as string.
- ggl: Opens a new window in default browser with given google query.
- start: Trying to start given program. If there is no such program in PATH does nothing.
- record: Provides speech to text in given file( format *.txt).
- open_and_write: Opens given file and writes from speech input.
- skype_call: Calling given name or tells that there is no registered user in contacts.txt.
"""
import speech_recognition as sr
import subprocess
import webbrowser
import pyglet
import os
import time
from gtts import gTTS

STOP_RECORDING = ['закончить запись', 'закончи запись']


def tell_and_die(speech='', name='1.mp3'):  # воспроизводит либо заданный текст, либо имеющуюся запись,
    if name == '1.mp3':                     # соответственно, если была подана запись,
                                            # то не имеет смысла добавлять какой-либо текст
        tts = gTTS(text=speech, lang='ru')
        tts.save("1.mp3")
        sound = pyglet.resource.media('1.mp3', streaming=False)
        sound.play()
        os.remove('1.mp3')
    else:
        sound = pyglet.resource.media(name, streaming=False)
        sound.play()


def get_word():  # считывает входящий поток с микрофона и переводит его в текст
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


def ggl():  # забивает весь поток с микрофона в гугл с открытием браузера
    tell_and_die(speech='Что найти?')
    while True:
        new_st = get_word()
        if new_st != '':
            break
    tell_and_die(name='share/recorded_sounds/sklonyayus-pered-vashej-volej.mp3')
    webbrowser.open('https://www.google.ru/search?q={0}&oq={1}&aqs=chrome.0.69i59j69i61.'
                    '775j0j8&sourceid=chrome&ie=UTF-8'.format(new_st, new_st))


def start():  # запускает программу по имени. Очень важно, чтобы данное имя имелось в переменной PATH,
              # и да, это пока только под винду. О том, как это должно работать под линуксом, пока не задумывался
    tell_and_die(speech='Какую программу запустить?')
    while True:
        new_st = get_word()
        if new_st != '':
            break
    try:
        with subprocess.Popen(' '.join(['start', new_st]), shell=True) as p:
            time.sleep(1)
            p.terminate()
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))


def record():
    tell_and_die(speech='В какой файл записать?')

    while True:
        print('Скажите название файла')
        new_st = get_word()
        if new_st != '':
            break
    try:
        file = open(''.join([new_st, '.txt']))
    except IOError:
        open_and_write(new_st)
    else:
        file.close()
        open_and_write(new_st, mode='a')


def open_and_write(file_name, mode='w'):
    with open(''.join([file_name, '.txt']), mode) as file:
        tell_and_die(speech='Запись началась')
        while True:
            new_st = get_word()
            if new_st.lower() in STOP_RECORDING:
                break
            else:
                if new_st != '':
                    file.write(new_st + '\n')
                    tell_and_die(speech='Продолжайте')
        tell_and_die(speech='Запись успешно завершена')
        file.write('\n')


def skype_call():
    tell_and_die(speech='Кому позвонить?')
    while True:
        new_st = get_word()
        if new_st != '':
            break
    try:
        with open('var/skype/contacts.txt', 'r') as f:
            for line in f:
                ans = line.split(' : ')
                if ans[0].lower() == new_st.lower():
                    print(ans[0], ans[-1])
                    new_st = ans[-1]
                    break
            else:  # если брейк не произошел
                tell_and_die(speech=' '.join(['Контакт', new_st, 'не найден, попробуйте еще раз']))
    except FileNotFoundError:
        tell_and_die(speech='Нет ни одного контакта. Необходимо добавить хотя бы один контакт')
    else:  # если не было исключения
        try:
            with subprocess.Popen(' '.join(['skype', '/callto:' + new_st]), shell=True) as p:
                time.sleep(1)
                p.terminate()
        except subprocess.CalledProcessError as e:
            print("Что-то пошло не так при запуске ({0})".format(e))


def respond(string):
    functionality = {['поиск', 'google', 'гугл', 'yandex', 'яндекс']: ggl,  # в идеале нужно сделать возможность,
                     'запуск': start, 'запись': record, 'skype': skype_call}  # чтобы можно было задавать это юзверю
    for i in functionality.keys():
        if string in i:
            return functionality[i]
    raise KeyError


def pseudo_main():
    tell_and_die('Приветствую! Ожидаю Ваших указаний')

    while True:
        st = get_word().lower()
        try:
            respond(st)()
        except KeyError:
            pass


if __name__ == '__main__':
    pseudo_main()
