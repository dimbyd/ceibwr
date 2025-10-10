# beiro.py
'''
Teclyn printio text lliwgar i'r terminal.
'''


class Beiro():

    def __init__(self):

        self.DIM = '\033[0m'
        self.DU = '\033[30m'
        self.COCH = '\033[31m'
        self.GWYRDD = '\033[32m'
        self.MELYN = '\033[33m'
        self.GLAS = '\033[34m'
        self.MAGENTA = '\033[35m'
        self.CYAN = '\033[36m'
        self.GWYN = '\033[37m'

    def disable(self):
        self.DIM = ''
        self.DU = ''
        self.COCH = ''
        self.GWYRDD = ''
        self.MELYN = ''
        self.GLAS = ''
        self.MAGENTA = ''
        self.CYAN = ''
        self.GWYN = ''

    def coch(self, s):
        return self.COCH + s + self.DIM if s else s

    def gwyrdd(self, s):
        return self.GWYRDD + s + self.DIM if s else s

    def melyn(self, s):
        return self.MELYN + s + self.DIM if s else s

    def glas(self, s):
        return self.GLAS + s + self.DIM if s else s

    def magenta(self, s):
        return self.MAGENTA + s + self.DIM if s else s

    def cyan(self, s):
        return self.CYAN + s + self.DIM if s else s

    def du(self, s):
        return self.DU + s + self.DIM if s else s

    def gwyn(self, s):
        return self.GWYN + s + self.DIM if s else s

    def write(self, s, lliw=None):
        if not lliw:
            return s
        elif lliw == 'b':
            return self.glas(s)
        elif lliw == 'g':
            return self.gwyrdd(s)
        elif lliw == 'r':
            return self.coch(s)
        elif lliw == 'c':
            return self.cyan(s)
        elif lliw == 'm':
            return self.magenta(s)
        elif lliw == 'y':
            return self.melyn(s)
        elif lliw == 'k':
            return self.du(s)
        elif lliw == 'w':
            return self.gwyn(s)
        else:
            return s


# ------------------------------------------------
def main():
    s = 'cranc'
    br = Beiro()
    sc = br.write(s, 'r')
    print(sc)
    # print(coch(s))
    # print(gwyrdd(s))
    # print(melyn(s))
    # print(glas(s))
    # print(magenta(s))
    # print(cyan(s))


if __name__ == '__main__': 
    main()
