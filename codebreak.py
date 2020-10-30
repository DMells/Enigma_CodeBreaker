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

    def codebreak1_reflector(self):
        self.name = 'codebreak1_reflector'
        reflectors = ['A','B','C']
        self.attempt = 0
        for reflector in reflectors:
            self.attempt += 1
            self.settings['reflector'] = reflector
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def codebreak2_positions(self):
        self.name = 'codebreak2_positions'
        positions = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.attempt = 0
        for position_combo in itertools.permutations(list(positions), 3):
            self.attempt += 1
            combo_as_list = [i for i in position_combo]
            self.settings['initial_positions'] = ' '.join(combo_as_list)
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def codebreak3_multi(self):
        self.name = 'codebreak3_multi'
        self.attempt = 0
        possible_rotors = ['Beta','Gamma','II','IV']
        possible_reflectors = ['A','B','C']
        allowed_digits = set('02468')
        possible_ring_settings = [i for i in range(1, 26) if set(str(i)) <= allowed_digits]
        for rotor_combo in itertools.permutations(possible_rotors, 3):
            for reflector in possible_reflectors:
                for ring_combo in itertools.permutations(possible_ring_settings, 3):
                    self.settings['rotors'] = ' '.join(list(rotor_combo))
                    self.settings['ring_settings'] = ' '.join(list((str(i) for i in ring_combo)))
                    self.settings['reflector'] = reflector
                    self.enigma = Enigma(self.settings)
                    self.enigma.create_machinery()
                    self.encode_write_output()

    def codebreak4_plugleads(self):
        self.name = "codebreak4_plugleads"

        self.attempt = 0
        # Search through plugboard_pairs and remove from possible_plug
        possible_plugs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for used_plug in self.settings['plugboard_pairs']:
            if used_plug in possible_plugs:
                possible_plugs = possible_plugs.replace(used_plug, '')

        for poss_pair in itertools.permutations(list(possible_plugs), 2):

            pairs = self.original_plugboard_pairs
            i = 0
            for char in range(len(pairs)):
                if pairs[char] == '?':
                    pairs = pairs[:char] + poss_pair[i] + pairs[char + 1:]
                    i += 1

            self.settings['plugboard_pairs'] = pairs
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def create_uniquepairssub(self,unique_pairs, two_pair):
        unique_pairs_sub = unique_pairs.copy()
        for i in two_pair:
            try:
                unique_pairs_sub.pop(unique_pairs_sub.index(i))
            except:
                import pdb
                pdb.set_trace()
                print("uh oh")
        return unique_pairs_sub

    def codebreak5_rewiring(self):
        self.name = "codebreak5_rewiring"
        # For each reflector
        reflectors = ['A','B','C']
        self.enigma = Enigma(self.settings)
        for reflector in reflectors:
            pins = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
            contacts = [i for i in self.enigma.rotor_box[reflector]['contacts']]
            #using max and min ensures the lettering is always in the same order, so can then create a set and get 13 uniques
            unique_pairs = list(set([max(i,j)+min(i,j) for (i, j) in zip(pins,contacts)]))
            unique_pairs = [[char for char in pair] for pair in unique_pairs]

            for two_pair in itertools.combinations(unique_pairs, 2):
                # Below gives two sets of combinations of re-wiring for the two pairs chosen
                possible_combos= [list(zip(each_permutation, list(two_pair[0]))) for each_permutation in itertools.permutations(list(two_pair[1]), 2)]
                # For each pair of tuples / combo
                for combo in possible_combos:
                    for two_pair2 in itertools.combinations(self.create_uniquepairssub(unique_pairs,two_pair), 2):
                        # Below gives two sets of combinations of re-wiring for the two pairs chosen
                        possible_combos2 = [list(zip(each_permutation, list(two_pair2[0]))) for each_permutation in
                                           itertools.permutations(list(two_pair2[1]), 2)]
                        # For each pair of tuples / combo
                        for combo2 in possible_combos2:

                            replacement_dict = {key: value for key, value in combo}
                            new_pins = pins.copy()
                            new_contacts = contacts.copy()
                            # Find the index of the key in pins, and replace that index in contacts with the value
                            for key, value in replacement_dict.items():
                                rep_id = new_pins.index(key)
                                new_contacts[rep_id] = value

                                rep_id = new_pins.index(value)
                                new_contacts[rep_id] = key

                            replacement_dict2 = {key: value for key, value in combo2}
                            # Find the index of the key in pins, and replace that index in contacts with the value
                            for key, value in replacement_dict2.items():
                                rep_id = new_pins.index(key)
                                new_contacts[rep_id] = value

                                rep_id = new_pins.index(value)
                                new_contacts[rep_id] = key

                        # rep_id = new_contacts.index(key)
                        # new_pins[rep_id] = value
                            self.settings['reflector'] = reflector
                            self.enigma = Enigma(self.settings)
                            self.enigma.rotor_box[reflector]['contacts'] = ''.join(new_contacts)
                            self.enigma.create_machinery()
                            self.attempt = 0
                            self.encode_write_output()
                            self.attempt +=1

    def encode_write_output(self):
        self.encoded_phrase = self.enigma.encode(self.code)
        # Encode 'code'
        if isinstance(self.crib, list):
            for crib in self.crib:
                if crib in self.encoded_phrase:
                    with open('codebreak.txt','a') as f:
                        f.write(f"Codebreak task: {self.name}\n\n")
                        f.write(f"Settings: \n")
                        f.write(f"{str(self.settings)}\n\n")
                        f.write(f"Input code : {self.code}\n")
                        f.write(f"Crib: {self.crib}\n")
                        f.write(f"Output code : {self.encoded_phrase}\n\n\n\n")
        else:
            if self.crib in self.encoded_phrase:
                with open('codebreak.txt', 'a') as f:
                    f.write(f"Codebreak task: {self.name}\n\n")
                    f.write(f"Settings: \n")
                    f.write(f"{str(self.settings)}\n\n")
                    f.write(f"Input code : {self.code}\n")
                    f.write(f"Crib: {self.crib}\n")
                    f.write(f"Output code : {self.encoded_phrase}\n\n\n\n")

                    # f.write(f"Output code : {self.encoded_phrase}\n")



if __name__ == '__main__':
    # CODE 1
    # settings = {'code':'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
    #             'crib': 'SECRETS',
    #             'rotors': 'Beta Gamma V',
    #             'reflector': 'UNKNOWN',
    #             'ring_settings': '04 02 14',
    #             'initial_positions':'M J M',
    #             'plugboard_pairs': 'KI XN FL'}
    # e = CodeBreaker(settings)
    # e.codebreak1_reflector()

    # CODE 2
    # settings = {'code':'CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH',
    #             'crib': 'UNIVERSITY',
    #             'rotors': 'Beta I III',
    #             'reflector': 'B',
    #             'ring_settings': '23 02 10',
    #             'initial_positions':'UNKNOWN',
    #             'plugboard_pairs': 'VH PT ZG BJ EY FS'}
    # e = CodeBreaker(settings)
    # e.codebreak2_positions()
    # CODE 3
    # settings = {'code':'ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY',
    #             'crib': 'THOUSANDS',
    #             'rotors': 'UNKNOWN',
    #             'reflector': 'UNKNOWN',
    #             'ring_settings': 'UNKNOWN',
    #             'initial_positions':'E M Y',
    #             'plugboard_pairs': 'FH TS BE UQ KD AL'}
    # e = CodeBreaker(settings)
    # e.codebreak3_multi()
    # CODE 4
    # settings = {'code': 'SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW',
    #             'crib':'TUTOR',
    #             'rotors':'V III IV',
    #             'reflector':'A',
    #             'ring_settings':'24 12 10',
    #             'initial_positions':'S W U',
    #             'plugboard_pairs': 'WP RJ A? VF I? HN CG BS'}
    # e = CodeBreaker(settings)
    # e.codebreak4_plugleads()
    # CODE 5
    settings = {'code': 'HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX',
                'crib':['FACEBOOK','INSTAGRAM','TWITTER','SNAPCHAT','YOUTUBE','REDDIT','LINKEDIN'],
                'rotors':'V II IV',
                'reflector':'A',
                'ring_settings':'6 18 7',
                'initial_positions':'A J L',
                'plugboard_pairs': 'UG IE PO NX WT'}
    e = CodeBreaker(settings)
    e.codebreak5_rewiring()
