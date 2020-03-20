from notifiers.notifier import Notifier

class PrintNotifier(Notifier):
    def __init__(self, fmt):
        self.fmt = fmt
    
    def notify(self, message):
        print(self.fmt.format(message))
