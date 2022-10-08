class SequenceGenerator:

    def __init__(self, start=0):
        self.start = 0

    def get(self):
        ret = self.start
        self.start += 1
        return ret

