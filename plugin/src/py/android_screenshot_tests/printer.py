class Printer:
    def __init__(self):
        self.SUCCESS = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.BOLD = '\033[1m'
        self.END = '\033[0m'

    def warning(self, text):
        print self.WARNING + text + self.END

    def success(self, text):
        print self.SUCCESS + text + self.END

    def fail(self, text):
        print self.FAIL + text + self.END

    def standard(self, text):
        print self.BOLD + text + self.END