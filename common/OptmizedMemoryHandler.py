from logging.handlers import MemoryHandler
import logging

class OptmizedMemoryHandler(MemoryHandler):
    def __init__(self, capacity, target):
        """ capacity: flush memory
            mail_subject: warning mail subject
            mail_host: the email host used
            mail_from: address send from; str
            mail_to: address send to; multi-addresses splitted by ';'

        """
        MemoryHandler.__init__(self, capacity, flushLevel=logging.ERROR, \
                                                target=target)
    def flush(self):
        """if flushed send mail
        """
        if self.buffer != [] and len(self.buffer) >= self.capacity:
            for record in self.buffer:
                self.target.handle(record)
            self.buffer = []