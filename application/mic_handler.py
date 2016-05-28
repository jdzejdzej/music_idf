from pyaudio import PyAudio, paInt16
import threading
import Queue


class MicHandler(threading.Thread):
    def __init__(self):
        super(MicHandler, self).__init__()
        self.daemon = True
        self.queue = Queue.Queue()
        self.stream = None
        self.end = False

    def pop(self):
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

    def qsize(self):
        return self.queue.qsize()

    def is_over(self):
        return self.end

    def listen(self):
        self.stream = PyAudio().open(format=paInt16, channels=1, rate=44100, input=True, frames_per_buffer=4096)
        self.start()

    def run(self):
        # py_audio = PyAudio()
        # stream = py_audio.open(format=paInt16, channels=1, rate=44100, input=True, frames_per_buffer=4096)
        time = 0.0
        while time < 30:
            data = self.stream.read(4096)
            self.queue.put_nowait((time, data))
            time += (4096 / 44100.0)
        self.end = True
