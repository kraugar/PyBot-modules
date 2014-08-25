import multiprocessing
import sys
import pyaudio
import wave
import time

from array import array
from struct import pack

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

class record(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.snd_started = False
        self.r = array('h')

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
            input=True, output=True,
            frames_per_buffer=CHUNK_SIZE)

        while True:

            snd_data = array('h', stream.read(CHUNK_SIZE))
            if sys.byteorder == 'big':
                snd_data.byteswap()

            silent = is_silent(snd_data)

            if not self.snd_started and not silent:
                print "\nStarted"
                self.snd_started = True
                self.r.extend(snd_data)

            if self.snd_started and silent and self.exit.is_set():
                self.r.extend(snd_data)
                break

            if self.snd_started:
                self.r.extend(snd_data)

        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        data = normalize(self.r)

        data = pack('<' + ('h'*len(data)), *data)

        wf = wave.open('demo.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

    def shutdown(self):
        print "Quiting"
        self.exit.set()

if __name__ == '__main__':
    p1 = record()
    while True:
        command = raw_input("> ").lower()

        if command != "" and command[0] == "s":
            p1.start()

        if command != "" and command[0] == "q":
            p1.shutdown()

        if command != "" and command[0] == "e":
            sys.exit()