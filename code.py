"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
Sources:https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/circuitpython-wiring-test
Adapted: Loreto Dumitrescu
"""
import board
import audiomp3
import audiopwmio
import time
from digitalio import DigitalInOut, Direction, Pull
import audiocore
import audiobusio
import neopixel


#Instance of audio output and sound file
audio = audiobusio.I2SOut(board.TX, board.RX, board.D9)
decoder = audiomp3.MP3Decoder(open("happy.mp3", "rb"))

#Instance of drawing pad
pad = DigitalInOut(board.A0)
pad.direction = Direction.INPUT
pad.pull = Pull.UP

#Instance of stop button
stop_button = DigitalInOut(board.A1)
stop_button.direction = Direction.INPUT
stop_button.pull = Pull.UP

#Instance of onboard pixel for visual feedback
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

#Variable to keep track of audio state
paused = False

def start_audio(audio, pixel, decoder):
    pixel.fill((100,100,100))
    audio.play(decoder)
    print("audio play")

def pause_audio(audio, pixel):
    audio.pause()
    print("audio pause")
    pixel.fill((0,0,255,))
    paused = True
    time.sleep(.1)

def resume_audio(audio, pixel):
    audio.resume()
    print("audio resume")
    pixel.fill((0,255,0,))
    time.sleep(.1)

def stop_audio(audio, pixel):
    audio.stop()
    print("audio stopped")
    pixel.fill((255,0,0,))
    time.sleep(.1)

def handle_press(audio, pixel, decoder, paused):
    if not audio.playing: # the first touch
        print("starting song")
        start_audio(audio, pixel, decoder)
    else:
        resume_audio(audio,pixel)

print('get the music started!')
while True:
    if not pad.value:
        handle_press(audio, pixel, decoder, paused)
    if pad.value and audio.playing:
        pause_audio(audio,pixel)
    if not stop_button.value:
        stop_audio(audio,pixel)
    time.sleep(.1)
