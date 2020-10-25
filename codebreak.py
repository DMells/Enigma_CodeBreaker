import enigma

class CodeBreaker(enigma):
    def __init__(self, settings):
        super().__init__.enigma()
        self.code = settings['code']
        self.crib = settings['crib']
        self.rotors = settings['rotors']
        self.reflector = settings['reflector']
        self.ringsettings = settings['ringsettings']
        self.positions = settings['positions']
        self.plugboardpairs = settings['plugboardpairs']


if __name__ == '__main__':
    settings = {'code':'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
                'crib': 'SECRETS',
                'rotors': 'Beta Gamma V',
                'reflector': 'UNKNOWN',
                'ringsettings': '04 02 14',
                'positions':'MJM',
                'plugboardpairs': 'KI XN FL'}
    e = CodeBreaker(settings)

    print(e)



"""
Could run through each, build where possible, and where not possible initiate a near-duplicate
class but one which iterates over all possibilities (given any restrictions)
Searches through the results using the crib, if there's a match, writes settings and result 
to a file, then continues and appends if any more matches.
"""