import threading
import ctypes

class KillableThread(threading.Thread):
    # Just creates a thread using the normal constructor with only a few specific arguments
    def __init__(self, target, args, name):
        super().__init__(target=target, args=args, name=name)

    # used in kill method to identify this thread
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # a method that tries to kill this thread. It only works sometimes and I don't really know why
    # but it is better than nothing. These threads will time out eventually on their own regardless
    def kill(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("thread killed")
