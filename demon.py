import speech_recognition as sr
import subprocess
import webbrowser


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
    while True:
        new_st = get_word()
        if new_st != '':
            break
    webbrowser.open('https://www.google.ru/search?q={0}&oq={1}&aqs=chrome.0.69i59j69i61.775j0j8&sourceid=chrome&ie=UTF-8'.format(new_st, new_st))


def start():
    while True:
        new_st = get_word()
        if new_st != '':
            break
    try:
        subprocess.run(["start", new_st], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Что-то пошло не так при запуске ({0})".format(e))

if __name__ == '__main__':
    while True:
        st = get_word()
        #print(st)
        if st == 'поиск':
            ggl()
        elif st == 'запуск':
            start()
