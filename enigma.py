from plugboard import Plugboard


class Rotor:
    def __init__(self,name, rotor_box, ring_setting, position, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right
        self.pins = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.contacts = rotor_box[name]['contacts']
        self.notch = rotor_box[name]['notch']
        self.ring_setting = int(ring_setting)
        self.position = position
        self.output_index = None
        self.encoded_char = None
        self.input_index = None

    def rotate(self, l, x):
        return l[x:] + l[:x]

    def adjust_starting_positions(self):
        # Adjust for starting position (rotates both pin and contact rings)
        if self.notch:
            print(f"Adjusting starting positions for {self.name}")
            num_position_rotations = ord('A') - ord(self.position)
            self.pins = self.rotate(self.pins, -num_position_rotations)
            self.contacts = self.rotate(self.contacts, -num_position_rotations)

            # Adjust for ring setting "-1" because ring_setting 1 is default
            self.contacts = self.rotate(self.contacts, -1 * (self.ring_setting-1))
            self.pins = self.rotate(self.pins, -1 * (self.ring_setting-1))

    def rotate_on_key_press(self):
        if self.notch:
            self.pins = self.rotate(self.pins, 1)
            self.contacts = self.rotate(self.contacts, 1)
            self.position = self.pins[0]
            self.previous_position = self.pins[-1]
            # Also update next left rotor if notch hit
            self.turnover()

    def rotor_encode_left(self, input_index):
        self.output_char = self.contacts[input_index]
        self.output_index = self.pins.index(self.output_char)
        # print(f"Rotor {self.name}, Pin: {self.pins[input_index]}, "
        #       f"Pin is mapped internally to Contact {self.output_char}")

    def rotor_encode_right(self, input_index):
        self.input_char = self.pins[input_index]
        self.output_index = self.contacts.index(self.input_char)
        self.output_char = self.pins[self.output_index]
        # print(f"Rotor {self.name}, Contact: {self.input_char}, "
        #       f"Contact is mapped internally to Pin {self.output_char}")

    def turnover(self):
        if self.previous_position == self.notch:
            print("Turnover triggered")
            nextrotor = self.left
            nextrotor.previous_position = nextrotor.pins[-1]
            nextnextrotor = nextrotor.left
            # while True:
                # If there is a nextrotor
            if nextrotor is not None:
                if nextrotor.notch:
                    if nextrotor.position != nextrotor.notch:
                        nextrotor.pins = self.rotate(nextrotor.pins, 1)
                        nextrotor.contacts = self.rotate(nextrotor.contacts, 1)
                        nextrotor.position = nextrotor.pins[0]
                    else:
                        print("Double Step")
                        # double-step
                        nextrotor.pins = self.rotate(nextrotor.pins, 1)
                        nextrotor.contacts = self.rotate(nextrotor.contacts, 1)
                        nextrotor.position = nextrotor.pins[0]

                        nextnextrotor.pins = self.rotate(nextnextrotor.pins, 1)
                        nextnextrotor.contacts = self.rotate(nextnextrotor.contacts, 1)
                        nextnextrotor.position = nextnextrotor.pins[0]
                # nextrotor = nextrotor.left



class Enigma:
    def __init__(self, settings):
        self.settings = settings
        self.root = None
        self.rotor_box = {
            "Housing": {'contacts': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'notch': None},
            "Beta": {'contacts': 'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'notch': None},
            "Gamma": {'contacts': 'FSOKANUERHMBTIYCWLQPZXVGJD', 'notch': None},
            "I": {'contacts': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},
            "II": {'contacts': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},
            "III": {'contacts': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'},
            "IV": {'contacts': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'notch': 'J'},
            "V": {'contacts': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'notch': 'Z'},
            "A": {'contacts': 'EJMZALYXVBWFCRQUONTSPIKHGD', 'notch': None},
            "B": {'contacts': 'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'notch': None},
            "C": {'contacts': 'FVPJIAOYEDRZXWGCTKUQSBNMHL', 'notch': None},
        }

        self.create_machinery()

    def create_machinery(self):
        # Add plugboard
        self.board = Plugboard(self.settings)
        # Add housing
        self.add("Housing")
        # Add rotors
        for i in range(len(self.settings['rotors'].split(' '))-1,-1, -1):
            rotor_name = self.settings['rotors'].split(' ')[i]
            ring_setting = self.settings['ring_settings'].split(' ')[i]
            initial_position = self.settings['initial_positions'].split(' ')[i]
            self.add(rotor_name, ring_setting, initial_position)
        # Add reflector
        self.add(self.settings['reflector'])

    def add(self, name, ring_setting=1, initial_position='A'):
        if self.root is None:
            self.root = Rotor(name, self.rotor_box, ring_setting, initial_position)
            self.root.adjust_starting_positions()
        else:
            ptr = self.root
            while True:
                if ptr.left is None:
                    ptr.left = Rotor(name, self.rotor_box, ring_setting, initial_position, right=ptr)
                    ptr.left.adjust_starting_positions()
                    break
                else:
                    ptr = ptr.left

    def encode(self, phrase):
        i=0
        encoded_phrase = []
        # For each character in the phrase
        while i < len(phrase):
            # New character, therefore reset ptr to root (housing)
            character = phrase[i]

            character = self.board.encode(character)

            ptr = self.root
            ptr.left.rotate_on_key_press()

            ptr.left.input_index = ptr.contacts.index(character.upper())
            ptr = ptr.left

            while True:
                # If there is another rotor to the left
                if ptr.left is not None:
                    if ptr.right.name == 'Housing':
                    # If we are at the first rotor
                        ptr.rotor_encode_left(ptr.input_index)
                    else:
                        # Else if there is a rotor to the right, grab that rotors encoded character
                        ptr.rotor_encode_left(ptr.right.output_index)
                    ptr = ptr.left
                else:
                    # No more rotors, now reflector
                    ptr.rotor_encode_left(ptr.right.output_index)
                    break
            # print("Reflector hit")
            ptr = ptr.right
            while True:
                if ptr.right:
                    # If we are at the first rotor
                    ptr.rotor_encode_right(ptr.left.output_index)
                    ptr = ptr.right
                else:
                    ptr.rotor_encode_right(ptr.left.output_index)
                    if self.board:
                        ptr.output_char = self.board.encode(ptr.output_char)
                    encoded_phrase.append(ptr.output_char)
                    break
            i+=1
        print(f"Input Phrase: {phrase}")
        print(f"Encoded Phrase: {''.join(encoded_phrase)}")
        return ''.join(encoded_phrase)


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    # MULTIPLE ROTOR DEMONSTRATION
    # 1 A -> U
    # 2 A -> B
    # 3 A -> L = means double step is correct
    # 4 Incorrect H gives M - should be Y - means ring settings are off OR the non-notch on Beta isnt working
    settings = {'rotors': "IV V Beta",
                'reflector': 'B',
                'ring_settings': '14 9 24',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.encode('H')
    # settings = {'rotors': "I II III IV",
    #             'reflector': 'B',
    #             'ring_settings': '14 9 24',
    #             'initial_positions': 'A A A',
    #             'plugboard_pairs': None}
    # e = Enigma(settings)
    # e.encode('H')

    #######################
    ##### EXAMPLE 1 #######
    #######################
    # settings = {'rotors': "I II III",
    #             'reflector': 'B',
    #             'ring_settings': '1 1 1',
    #             'initial_positions': 'A A Z',
    #             'plugboard_pairs': 'HL MO AJ CX BZ SR NI YW DG PK'}
    # e = Enigma(settings)
    # e.encode('HELLOWORLD')

    #######################
    ##### EXAMPLE 2 #######
    #######################
    # settings = {'rotors': "IV V Beta I",
    #             'reflector': 'A',
    #             'ring_settings': '18 24 3 5',
    #             'initial_positions': 'E Z G P',
    #             'plugboard_pairs': 'PC XZ FM QA ST NB HY OR EV IU'}
    # e = Enigma(settings)
    # e.encode('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI')





    # settings = {'rotors': "III II I",
    #             'reflector': 'B',
    #             'ring_settings': '1 1 1',
    #             'initial_positions': 'A A A',
    #             'plugboard_pairs': None
    #              }
    # e = Enigma(settings)
    # e.encode("AAAAAAAAAAAAAAAAAAAAAAAAAA")



    # c = enigma_config(board)
    # c.add("Housing")
    # c.add("III",ring_setting=1, initial_position='Z')
    # c.add("II",ring_setting=1, initial_position='A')
    # c.add("I", ring_setting=1, initial_position='A')
    # c.add("B")
    # c.encode("HELLOWORLD")

    # DOES NOT WORK - SHOULD GIVE 'V' BUT GIVES 'Y'
    # c = enigma_config()
    # c.add("Housing")
    # c.add("IV",ring_setting=19, initial_position='Z')
    # c.add("III",ring_setting=15, initial_position='V')
    # c.add("II",ring_setting=11, initial_position='E')
    # c.add("I", ring_setting=7, initial_position='Q')
    # c.add("C")
    # c.encode("Z")

    # c.add("Housing")
    # c.add("Beta", ring_setting=24, initial_position='A')
    # c.add("V", ring_setting=9, initial_position='A')
    # c.add("IV", ring_setting=14, initial_position='A')
    # c.add("B")
    # c.encode("H")

    ################################
    #ENIGMA DEMONSTRATION EXAMPLE 1
    ################################
    # board = Plugboard()
    # board.add(PlugLead("HL"))
    # board.add(PlugLead("MO"))
    # board.add(PlugLead("AJ"))
    # board.add(PlugLead("CX"))
    # board.add(PlugLead("BZ"))
    # board.add(PlugLead("SR"))
    # board.add(PlugLead("NI"))
    # board.add(PlugLead("YW"))
    # board.add(PlugLead("DG"))
    # board.add(PlugLead("PK"))
    # print(board.encode(""))
    #
    # c = enigma_config(board)
    # c.add("Housing")
    # c.add("III", ring_setting=1, initial_position='Z')
    # c.add("II", ring_setting=1, initial_position='A')
    # c.add("I", ring_setting=1, initial_position='A')
    # c.add("B")
    # c.encode("HELLOWORLD")

    ################################
    # ENIGMA DEMONSTRATION EXAMPLE 2
    ################################






    # Assert pluglead.mapping length == 2, "Cannot plug into more than one letter"
    # Assert pluglead.mapping not a double i.e. "EE", "cannot physically connect a letter to itself as there is only one plugboard space per letter"
    # Assert pluglead.mapping doesn't already exist in a different pluglead instance.

# Notes
"""
Check that the ord(A) - ord(blah) works for long sentences, might fall over 
"""
"""
Advanced Ideas
- Removing limitation of being able to crack the code by allowing plugboard letter able to plug into itself (this was how Turing cracked the code)
- Or able to plug a threeway lead with a random chance of 
- Could add arg parsing to initiate advanced mode
- use of decorators?
- could ensure plugleads are not identical by defining __eq__ - it's more complicated but looks better
- user interface ? ("How many leads? input :" "Please type X mappings") etc
- Multiple inheritance for encode methods? (duplicated but might not be doing same thing)
- Need to check if rotor has already been taken out of the box and used in the machine
-- Multiple plugboards? Have an enigma() parent class
Could add plugboard and housing as part of abstract base class? (will always need to add these)
"""