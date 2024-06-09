from threading import Timer

class TimerAndResult(Timer):
    def __init__(self, time_delay, function, args=[]):
        self.input_function = function
        super().__init__(time_delay, self.execute_function, args)

    def execute_function(self, *a):
        self.result = self.input_function(*a)

    def join(self):
        super().join()
    
    def output(self):
        return {'message_id': self.result}

