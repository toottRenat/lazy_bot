
"""
Фактически этот файл не нужен, сделал лишь на всякий случай
"""

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

textToSearch = 'hello world'
query = urllib.parse.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
    print('https://www.youtube.com' + vid['href'])