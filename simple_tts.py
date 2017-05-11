from gtts import gTTS
import pyglet

tts = gTTS(text='Good morning', lang='en')
tts.save("good.mp3")
song = pyglet.media.load('good.mp3')
song.play()
pyglet.app.run()
