import quopri
import base64
from email.header import Header, decode_header, make_header
import numpy as np
from imaplib import IMAP4, IMAP4_SSL

server = IMAP4_SSL('imap.mail.ru')
mail = 'basonchik@mail.ru'
email_pass = 'Ythtyj5623'
server.login(mail, email_pass)

server.select()
result, ids = server.search(None, '(UNSEEN)')

print("New emails with your email in TO is %d" % len(ids[0].split()))

i = 0


def find_encoding(byte_string):
    """
    Почувствуй себя либой, предоставляющей регулярные выражения
    """
    st = ''
    for i, ch in enumerate(byte_string):
        if chr(ch) == '=' and chr(byte_string[i + 1]) == '?':
            #print('in if')
            n_questions = 0
            j = i
            while chr(byte_string[j]) != '?' or n_questions != 2:
                #print('in while')
                if chr(byte_string[j]) == '?':
                    n_questions += 1
                st += chr(byte_string[j])
                j += 1
            break
    return st[2:-2], st[-1]


for e_id in ids[0].split()[::-1]:
    i += 1
    subject = server.fetch(e_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')[1][0][1].strip()
    #print(quopri.decodestring(subject)[8:30].lower())
    h = make_header(decode_header(quopri.decodestring(subject)))
    print(str(h))
    #print(find_encoding(quopri.decodestring(subject).lower()))
    #encoding, t = find_encoding(quopri.decodestring(subject).lower())
    #if t == 'b':
        #print(type(quopri.decodestring(subject)))
        #print("\t" + base64.decodebytes(quopri.decodestring(subject)))
    #else:
        #print("\t" + quopri.decodestring(subject).decode(encoding))
    #print(b'=?utf-8?b' in quopri.decodestring(subject)[8:26].lower())
    #print("\t" + str(quopri.decodestring(subject), encoding))  # koi8_r, UTF-8, cp1251
    #print("\t" + quopri.decodestring(subject.encode('utf-8')).decode('utf-8'))
    if i == 300:
        break
