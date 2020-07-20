import time
from collections import defaultdict


class SimpleLogger:

    class Msg:
        def __init__ (self, text, priority):
            self.text = text
            self.priority = priority


    def __init__ (self):
        self.timers = {}
        self.log_msgs = []


    def time_stamp_start(self, name):
        if name in self.timers.keys():
            self.log_msg("Timer already running: " + str(name))
        else:
            start_time = time.time()
            self.timers[name] = start_time
            self.log_msg("Timer Started: " + str(name), 1)
            

    def time_stamp_stop(self, name):
        if name not in self.timers.keys():
            self.log_msg("Trying to stop non-existant timer " + str(name))
            return None
        else:
            duration = time.time() - self.timers[name]
            del self.timers[name]
            self.log_msg("Duration: " + str(name) + " = " + str(duration))
            return duration

    def time_stamp_start_and_print(self, name):
        self.time_stamp_start(name)
        print(name + " : running")

    def time_stamp_stop_and_print(self, name):
        duration = self.time_stamp_stop(name)
        print(name + " : " + str(duration) + " seconds")


    def log_msg(self, msg, priority = 0):
        self.log_msgs.append(self.Msg(msg, priority))
    
    def print_log(self, priority = float('inf')):
        for msg in self.log_msgs:
            if msg.priority < priority:
                print(msg.text)

    def log_clear(self):
        self.log_msgs = defaultdict(list)




def unit_tests():

    logger = SimpleLogger()
    logger.time_stamp_start("spinner")
    for i in range(0, 1000000):
        i = i
        continue
    time = logger.time_stamp_stop("spinner")
    print(time)

    logger.log_msg("Test msg no priority")
    logger.log_msg("Test msg priority 0", 0)
    logger.log_msg("Test msg priority 1", 1)
    logger.log_msg("Test msg priority 2", 2)

    logger.print_log(1)
    print()
    logger.print_log()
    print()
    logger.log_clear()


def main():
    unit_tests()

