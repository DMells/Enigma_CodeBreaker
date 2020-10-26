from enigma import Enigma
import itertools

class CodeBreaker:
    def __init__(self, settings):
        self.settings = settings
        self.code = settings['code']
        self.crib = settings['crib']
        self.rotors = settings['rotors']
        self.reflector = settings['reflector']
        self.ring_settings = settings['ring_settings']
        self.initial_positions = settings['initial_positions']
        self.original_plugboard_pairs = settings['plugboard_pairs']

    def codebreak_plugleads(self):

        self.attempt = 0
        # Search through plugboard_pairs and remove from possible_plug
        possible_plugs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for used_plug in self.settings['plugboard_pairs']:
            if used_plug in possible_plugs:
                possible_plugs = possible_plugs.replace(used_plug,'')

        for poss_pair in itertools.permutations(list(possible_plugs), 2):

            pairs = self.original_plugboard_pairs
            i = 0
            for char in range(len(pairs)):
                if pairs[char]=='?':
                    pairs = pairs[:char] + poss_pair[i] + pairs[char + 1:]
                    i+=1

            self.settings['plugboard_pairs'] = pairs
            self.enigma = Enigma(self.settings)
            self.encode_write_output()


    def codebreak_reflector(self):
        reflectors = ['A','B','C']
        self.attempt = 0
        for reflector in reflectors:
            self.attempt += 1
            self.settings['reflector'] = reflector
            self.enigma = Enigma(self.settings)
            self.encode_write_output()


    def encode_write_output(self):
        self.encoded_phrase = self.enigma.encode(self.code)
        # Encode 'code'
        if self.crib in self.encoded_phrase:
            with open('codebreak.txt','a') as f:
                f.write(f"Codebreak attempt {self.attempt}\n\n")
                f.write(f"Settings: \n")
                f.write(f"{self.settings}\n\n")
                f.write(f"Input code : {self.code}\n")
                f.write(f"Crib: {self.crib}\n")
                f.write(f"Output code : {self.encoded_phrase}\n\n\n\n")


if __name__ == '__main__':
    # CODE 1
    settings = {'code':'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
                'crib': 'SECRETS',
                'rotors': 'Beta Gamma V',
                'reflector': 'UNKNOWN',
                'ring_settings': '04 02 14',
                'initial_positions':'M J M',
                'plugboard_pairs': 'KI XN FL'}
    e = CodeBreaker(settings)
    e.codebreak_reflector()

    # CODE 2

    # CODE 3

    # CODE 4
    # settings = {'code': 'SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW',
    #             'crib':'TUTOR',
    #             'rotors':'V III IV',
    #             'reflector':'A',
    #             'ring_settings':'24 12 10',
    #             'initial_positions':'S W U',
    #             'plugboard_pairs': 'WP RJ A? VF I? HN CG BS'}
    # e = CodeBreaker(settings)
    # e.codebreak_plugleads()

"""
Could run through each, build where possible, and where not possible (try except?) initiate a near-duplicate
class but one which iterates over all possibilities (given any restrictions)
Searches through the results using the crib, if there's a match, writes settings and result 
to a file, then continues and appends if any more matches.
"""