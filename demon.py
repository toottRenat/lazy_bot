import speech_recognition as sr
import subprocess
import webbrowser
import pyglet
import os
from gtts import gTTS


def tell_and_die(speech='ахаха', name='1.mp3'):
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
    while True:
        new_st = get_word()
        if new_st != '':
            break
    try:
        #subprocess.run(["start", new_st], shell=True, check=True)
        p = subprocess.Popen(["start", new_st], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()
        print(output)
        print('-----------')
        print(errors)
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))

if __name__ == '__main__':
    while True:
        st = get_word()
        # print(st)
        if st == 'поиск':
            ggl()
        elif st == 'запуск':
            start()