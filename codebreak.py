from enigma import Enigma
import itertools


class CodeBreaker:
    """
    Contains separate functions to run each of the codebreaker tasks, as well as a writer function to output results
    to a text file
    """
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
        """
        Searches through all reflectors to find the settings which contain the crib in the decoded message
        """
        self.name = 'codebreak1_reflector'
        self.attempt = 1
        reflectors = ['A','B','C']

        for reflector in reflectors:
            self.settings['reflector'] = reflector
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def codebreak2_positions(self):
        """
        Searches through every possible rotor position to find the settings which produce the crib in the decoded message
        """
        self.name = 'codebreak2_positions'
        self.attempt = 1
        positions = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # Iterate over every possible trio of positions
        for trio in itertools.permutations(list(positions), 3):
            # Convert trio to a list
            trio_as_list = [i for i in trio]
            # Convert list to space-separated string and assign to settings dictionary
            self.settings['initial_positions'] = ' '.join(trio_as_list)
            # Run enigma with given settings and write results
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def codebreak3_multi(self):
        """
        Searches through every possible combination of rotor, positions, and ring settings to find the
        settings which produce the crib in the decoded message
        """
        self.name = 'codebreak3_multi'
        self.attempt = 1
        possible_rotors = ['Beta','Gamma','II','IV']
        possible_reflectors = ['A','B','C']
        # Odd numbers not allowed
        allowed_digits = set('02468')
        # Get list of all possible ring settings
        possible_ring_settings = [i for i in range(1, 26) if set(str(i)) <= allowed_digits]

        # Iterate over each trio of possible rotor combinations
        # For each rotor combination...
        for rotor_combo in itertools.permutations(possible_rotors, 3):
            # ...and for each reflector...
            for reflector in possible_reflectors:
                #...and for each trio of possible ring settings...
                for ring_combo in itertools.permutations(possible_ring_settings, 3):
                    self.settings['rotors'] = ' '.join(list(rotor_combo))
                    self.settings['ring_settings'] = ' '.join(list((str(i) for i in ring_combo)))
                    self.settings['reflector'] = reflector
                    # ...run enigma and write output
                    self.enigma = Enigma(self.settings)
                    self.enigma.create_machinery()
                    self.encode_write_output()

    def codebreak4_plugleads(self):
        """
        Searches through the different possible missing plugleads to find the settings which produce the
        crib in the decoded message
        """
        self.name = "codebreak4_plugleads"
        self.attempt = 1
        possible_plugs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Amend possible_plugs to remove any already-used plugs
        for used_plug in self.settings['plugboard_pairs']:
            if used_plug in possible_plugs:
                possible_plugs = possible_plugs.replace(used_plug, '')

        # For each possible remaining plug pair...
        for plug_pair in itertools.permutations(list(possible_plugs), 2):
            pairs = self.original_plugboard_pairs
            i = 0
            # For each character in the original string of plug pairs (contains '?')
            for char in range(len(pairs)):
                if pairs[char] == '?':
                    # Swap the '?' for one of the remaining possible plugs
                    pairs = pairs[:char] + plug_pair[i] + pairs[char + 1:]
                    i += 1
            # Update settings to reflect the new plug pairs list and run through Enigma
            self.settings['plugboard_pairs'] = pairs
            self.enigma = Enigma(self.settings)
            self.enigma.create_machinery()
            self.encode_write_output()

    def codebreak5_rewiring(self):
        """
        Searches through every possible reflector re-wiring combination to find the settings which produce an decoded
        message containing one of the cribs. There are 8 possible character changes/rewirings, which means two sets of
        swaps.
        This function finds the first possible set of rewirings (2 plugleads / 4 plugs), then iterates to find a
        second possible set, and runs them into Enigma.
        Once all of the possible second sets have been exhausted, the function will change the first set and iterate
        again over all second sets, ensuring that the two sets are never the same to save time.
        """
        self.name = "codebreak5_rewiring"
        self.attempt = 1
        reflectors = ['A','B','C']
        # Establish a dummy enigma instance to iteratively be able to get access to the different reflector contacts lists
        self.enigma = Enigma(self.settings)

        # For each reflector...
        for reflector in reflectors:
            pins = [i for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

            # ...get the contacts for that reflector (list of characters A-Z unordered)
            contacts = [i for i in self.enigma.rotor_box[reflector]['contacts']]

            # using max and min ensures the lettering is always in the same order, so can then create a set and get
            # 13 unique pairs of reflector mappings
            unique_pairs = list(set([max(i,j)+min(i,j) for (i, j) in zip(pins,contacts)]))
            unique_pairs = [[char for char in pair] for pair in unique_pairs]

            # For every possible duo of reflector mappings...
            for mappings_duo in itertools.combinations(unique_pairs, 2):
                #...create an iterator which will give all possible combinations of re-wiring for the duo of mappings
                possible_rewirings= [list(zip(each_permutation, list(mappings_duo[0]))) for each_permutation in \
                                  itertools.permutations(list(mappings_duo[1]), 2)]

                # For each rewired pair...
                for rewired_pair in possible_rewirings:
                    # ...do the same for a second pair. create_uniquepairssub() removes the already-used duo to avoid
                    # using the same rewired_pair twice.
                    for mappings_duo2 in itertools.combinations(self.create_uniquepairssub(unique_pairs,mappings_duo), 2):
                        possible_rewirings2 = [list(zip(each_permutation, list(mappings_duo2[0]))) for each_permutation in
                                           itertools.permutations(list(mappings_duo2[1]), 2)]

                        # For each second set of re-wired pairs...
                        for rewired_pair2 in possible_rewirings2:
                            # Use the first rewired pair to create a dictionary of mappings
                            replacement_dict = {key: value for key, value in rewired_pair}
                            new_pins = pins.copy()
                            new_contacts = contacts.copy()

                            # Find the index of the key in pins, and replace that index in the reflector contacts with
                            # the value in the replacement dictionary
                            for key, value in replacement_dict.items():
                                rep_id = new_pins.index(key)
                                new_contacts[rep_id] = value

                                rep_id = new_pins.index(value)
                                new_contacts[rep_id] = key

                            # Do the same for the second set of rewired pairs
                            replacement_dict2 = {key: value for key, value in rewired_pair2}
                            for key, value in replacement_dict2.items():
                                rep_id = new_pins.index(key)
                                new_contacts[rep_id] = value

                                rep_id = new_pins.index(value)
                                new_contacts[rep_id] = key

                            # Update settings dictionary to contain the update reflector contacts and run through enigma
                            self.settings['reflector'] = reflector
                            self.enigma = Enigma(self.settings)
                            self.enigma.rotor_box[reflector]['contacts'] = ''.join(new_contacts)
                            self.enigma.create_machinery()
                            self.encode_write_output()

    def create_uniquepairssub(self,unique_pairs, two_pair):
        """ Used in codebreak5, removes the already-used duo to avoid using the same rewired_pair twice"""
        unique_pairs_sub = unique_pairs.copy()
        for i in two_pair:
            unique_pairs_sub.pop(unique_pairs_sub.index(i))
        return unique_pairs_sub

    def encode_write_output(self):
        # Run code through enigma using derived settings
        self.encoded_phrase = self.enigma.encode(self.code)

        # If there are multiple inputs in the crib, iterate over them before checking through the encoded phrase
        if isinstance(self.crib, list):
            for crib in self.crib:
                if crib in self.encoded_phrase:
                    with open('codebreak.txt','a') as f:
                        self.write(f)
                    self.attempt += 1
        else:
            if self.crib in self.encoded_phrase:
                with open('codebreak.txt', 'a') as f:
                    self.write(f)
                self.attempt+=1

    def write(self, f):
        """ Specify formatting of each output to codebreak.txt """
        if self.attempt ==1:
            f.write(f"#################################\n")
            f.write(f"Codebreak task: {self.name}\n")
            f.write(f"#################################\n\n")

        f.write(f"Attempt : {self.attempt}\n")
        f.write(f"SETTINGS: \n")
        f.write(f"Rotors : {str(self.settings['rotors'])}\n")
        f.write(f"Initial Positions : {str(self.settings['initial_positions'])}\n")
        f.write(f"Ring Settings : {str(self.settings['ring_settings'])}\n")
        f.write(f"Reflector : {str(self.settings['reflector'])}\n")
        f.write(f"Plugboard Pairs : {str(self.settings['plugboard_pairs'])}\n\n")
        f.write(f"Input code : {self.code}\n")
        f.write(f"Crib: {self.crib}\n")
        f.write(f"Output code : {self.encoded_phrase}\n\n\n\n")

