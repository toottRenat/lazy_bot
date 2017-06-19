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
- record: Provides speech to text in given file (format *.txt).
- open_and_write: Opens given file and writes from speech input.
- skype_call: Calling given name or tells that there is no registered user in contacts.txt.
- ...

В идеале нужно подрубить семантический поиск и все в этом роде, чтобы сделать нечто универсальное,
и распозновать все из одной большой фразы, а не несколько маленьких
"""

import os
import time
import pyglet
import random
import urllib
import subprocess
import webbrowser
import timeout_decorator
import speech_recognition as sr

from gtts import gTTS
from mutagen.mp3 import MP3

from lib.vk import vk_stuff


PREFIX = ''
STOP_RECORDING = ('закончить запись', 'закончи запись')


def tell_and_die(speech='', name='1.mp3'):
    """
    Воспроизводит либо заданный текст, либо имеющуюся запись,
    соответственно, если была подана запись,
    то не имеет смысла добавлять какой-либо текст
    """
    if name == '1.mp3':
        tts = gTTS(text=speech, lang='ru')
        tts.save("1.mp3")
        sound = pyglet.resource.media('1.mp3', streaming=False)
        sound.play()
        os.remove('1.mp3')
    else:
        sound = pyglet.resource.media(name, streaming=False)
        sound.play()


# @timeout_decorator.timeout(5)
def get_word():
    """
    Считывает входящий поток с микрофона и переводит его в текст
    """
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


def wait_for_word(st):
    tell_and_die(speech=st)
    while True:
        new_st = get_word()
        if new_st != '':
            break
    return new_st


def ggl():
    """
    Забивает весь поток с микрофона в гугл с открытием браузера
    """
    new_st = wait_for_word('Что найти?')
    tell_and_die(name='share/recorded_sounds/sklonyayus-pered-vashej-volej.mp3')
    webbrowser.open('https://www.google.ru/search?q={0}&oq={1}&aqs=chrome.0.69i59j69i61.'
                    '775j0j8&sourceid=chrome&ie=UTF-8'.format(new_st, new_st))


def start():
    """
    Запускает программу по имени. Очень важно, чтобы данное имя имелось в переменной PATH,
    и да, это пока только под винду. О том, как это должно работать под линуксом, пока не задумывался
    """
    new_st = wait_for_word('Какую программу запустить?')
    try:
        with subprocess.Popen(' '.join(['start', new_st]), shell=True) as p:
            time.sleep(1)
            p.terminate()
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))


def record():
    new_st = wait_for_word('В какой файл записать?')
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
    skype_conf_file = ''.join([PREFIX, 'var/skype/contacts.txt'])
    new_st = wait_for_word('Кому позвонить?')
    try:
        new_st = get_line(skype_conf_file, new_st,
                          ' '.join(['Контакт', new_st, 'не найден, попробуйте еще раз']))
    except NameError:
        return
    except FileNotFoundError:
        tell_and_die(speech='Нет ни одного контакта. Необходимо добавить хотя бы один контакт')
    else:  # если не было исключения
        try:
            with subprocess.Popen(' '.join(['skype', '/callto:' + new_st]), shell=True) as p:
                time.sleep(1)
                p.terminate()
        except subprocess.CalledProcessError as e:
            print("Что-то пошло не так при запуске ({0})".format(e))


def youtube():
    new_st = wait_for_word('Какое видео найти?')
    query = urllib.parse.quote(new_st)
    url = "https://www.youtube.com/results?search_query=" + query
    tell_and_die(name='share/recorded_sounds/sklonyayus-pered-vashej-volej.mp3')
    webbrowser.open(url)


def play_music():  # todo
    # Обновляет запись, по истечении времени, отведенного на воспроизведение.
    # Если делать перемотку, то будут небольшие проблемы, а так норм.
    music_conf_file = ''.join([PREFIX, 'var/conf/play_music_config.txt'])
    new_st = 'zz'
    #new_st = wait_for_word('Какого исполнителя запустить?')
    try:
        new_st = get_line(music_conf_file, new_st,
                          ' '.join(['Исполнитель', new_st, 'не найден, попробуйте еще раз']))
    except NameError:
        return
    else:
        music_files = os.listdir(new_st)  # сделать рекурсивый просмотр директорий
        random_mf = []
        print(music_files)

        while len(music_files) > 0:  # перемешивает композиции
            i = random.randint(0, len(music_files) - 1)
            random_mf.append(music_files[i])
            music_files.pop(i)

        print(random_mf)
    try:
        for i in music_files:
            with subprocess.Popen(' '.join(['start wmplayer /close',
                                            '\\'.join([new_st, i])]),
                                  shell=True) as p:
                audio = MP3('\\'.join([new_st, i]))
                print(audio.info.length)
                time.sleep(audio.info.length)
                p.terminate()
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))


def vk_message():
    vk_message_conf_file = ''.join([PREFIX, 'var/conf/vk_message_config.txt'])
    user = wait_for_word('Кому написать?')

    try:
        user = get_line(vk_message_conf_file, user,
                        ' '.join(['Контакт', user, 'не найден, попробуйте еще раз']))
    except NameError:
        return

    tell_and_die(speech='Что написать?')
    while True:
        message = get_word()
        if message != '':
            break

    vk_stuff.main(user, message)


def get_line(file, new_st, ans):
    with open(file, 'r') as f:
        for line in f:
            ans = line.split(' : ')
            if ans[0].lower() == new_st.lower():
                new_st = ans[-1]
                break
        else:  # если брейк не произошел
            tell_and_die(speech=ans)
            raise NameError
    return new_st


def respond(string):
    functionality = get_functionality()
    for i in functionality.keys():
        if string in functionality[i]:
            return i
    raise KeyError


def get_functionality():
    start_conf_file = ''.join([PREFIX, 'var/conf/start_config.txt'])
    search_conf_file = ''.join([PREFIX, 'var/conf/search_config.txt'])
    record_conf_file = ''.join([PREFIX, 'var/conf/record_config.txt'])
    skype_call_conf_file = ''.join([PREFIX, 'var/conf/skype_call_config.txt'])
    youtube_conf_file = ''.join([PREFIX, 'var/conf/youtube_config.txt'])
    vk_conf_file = ''.join([PREFIX, 'var/conf/vk_config.txt'])

    files = (start_conf_file, search_conf_file, record_conf_file,
             skype_call_conf_file, youtube_conf_file, vk_conf_file)
    commands = (start, ggl, record,
                skype_call, youtube, vk_message)
    func = {}
    for i, file in enumerate(files):
        try:
            with open(file, 'r') as f:
                arr = []
                for line in f:
                    arr.append(line.strip())
            if len(arr) > 0:
                func[commands[i]] = arr
            else:
                print(' '.join(['Файл', file, 'пустой, необходимо заполнить его хоть чем-то']))
        except FileNotFoundError:
            print(' '.join(['Файл', file, 'не найден, создаю данный файл']))
            f = open(file, 'w')
            f.close()
    return func


def pseudo_main():
    # сделать максимально через 1 фразу, даже без семантического поиска
    tell_and_die('Приветствую! Ожидаю Ваших указаний.')

    while True:
        st = get_word().lower()
        try:
            respond(st)()
        except KeyError:
            pass


if __name__ == '__main__':
    play_music()
    #pseudo_main()
