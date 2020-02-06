class QssLoader:
    def __init__(self):
        pass

    @staticmethod
    def loadQss(style):
        with open(style,'r') as f:
            return f.read()