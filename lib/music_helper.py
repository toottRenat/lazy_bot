"""
Может пригодиться впоследствии.
С той логикой, какая есть сейчас, избыточен.
"""

import os


PREFIX = '../'
PATHS = ''.join([PREFIX, 'var/conf/play_music_config.txt'])


paths = [line.strip() for line in open(PATHS, 'r')]
# print(paths)


def find_dir(st):
    for i in paths:
        os.chdir(i)
