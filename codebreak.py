from enigma import Enigma

class CodeBreaker(Enigma):
    def __init__(self, settings):
        # super.__init__(self, settings)
        self.code = settings['code']
        self.crib = settings['crib']
        self.rotors = settings['rotors']
        self.reflector = settings['reflector']
        self.ring_settings = settings['ring_settings']
        self.initial_positions = settings['initial_positions']
        self.plugboardpairs = settings['plugboardpairs']


if __name__ == '__main__':
    settings = {'code':'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
                'crib': 'SECRETS',
                'rotors': 'Beta Gamma V',
                'reflector': 'UNKNOWN',
                'ring_settings': '04 02 14',
                'initial_positions':'MJM',
                'plugboardpairs': 'KI XN FL'}
    e = CodeBreaker(settings)
    f =
    print(e)



"""
Could run through each, build where possible, and where not possible (try except?) initiate a near-duplicate
class but one which iterates over all possibilities (given any restrictions)
Searches through the results using the crib, if there's a match, writes settings and result 
to a file, then continues and appends if any more matches.
"""