import threading
from kivy.clock import Clock

class ThreadedFunctionRunner:
    def __init__(self, func, keep_args, args_list, callback):
        self.func = func
        self.keep_args = keep_args
        self.args_list = args_list
        self.callback = callback
        self.results = [self.keep_args, {"username": "", "password": ""}]
        self.threads = []

    def start(self):
        for args in self.args_list:
            thread = threading.Thread(target=self.run, args=args)
            self.threads.append(thread)
            thread.start()

    def run(self, *args):
        id = args[0]
        username = args[1]
        password = args[2]
        result = self.func(username, password)
        self.results[1][id] = result

        if self.results[1]["username"] != "" and self.results[1]["password"] != "":
            if self.callback:
                Clock.schedule_once(lambda dt: self.callback(self.results))