import time


class Animation:
    def __init__(self):
        self.counter = 1
        self.running = True

    def display(self):
        return self.counter

    def loading(self):
        while self.running:
            self.counter += 1
            if self.counter > 8:
                self.counter = 1
            time.sleep(0.1)
