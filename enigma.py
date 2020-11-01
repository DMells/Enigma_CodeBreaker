from plugboard import Plugboard
import string


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
            self.root.adjust_ring_setting()
            self.root.adjust_starting_positions()
        else:
            ptr = self.root
            while True:
                if ptr.left is None:

                    ptr.left = Rotor(name, self.rotor_box, ring_setting, initial_position, right=ptr)
                    ptr.left.adjust_ring_setting()
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
            ptr.left.key_press()

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
        if len(self.settings['rotors'].split(' ')) ==3:
            print(
                f'Final Rotor/Reflector Positions:{self.root.left.left.left.position}{self.root.left.left.position}{self.root.left.position}')
        else:
            print(f'Final Rotor/Reflector Positions:{self.root.left.left.left.left.position}{self.root.left.left.left.position}{self.root.left.left.position}{self.root.left.position}')
        return ''.join(encoded_phrase)

class Rotor:
    def __init__(self,name, rotor_box, ring_setting=1, position='A', left=None, right=None):
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

    def reorder(self, l, x):
        return l[x:] + l[:x]

    def adjust_starting_positions(self):
        # Adjust for starting position (rotates both pin and contact rings)
        if self.name not in ['A','B','C']:
            num_position_rotations = (string.ascii_uppercase.index('A') + string.ascii_uppercase.index(self.position)) % 26
            self.pins = self.reorder(self.pins, num_position_rotations)
            self.contacts = self.reorder(self.contacts, num_position_rotations)

    def adjust_ring_setting(self):
        # Get initial offsets
        self.offsets = []
        for (pin, contact) in zip(self.pins, self.contacts):
            self.offsets.append(string.ascii_uppercase.index(contact) - string.ascii_uppercase.index(pin))

        self.offsets = self.reorder(self.offsets, -1 * (self.ring_setting - 1))
        self.old_contacts = self.contacts
        self.contacts = []
        d = dict(enumerate(string.ascii_uppercase, 0))
        for i, (pin, offset) in enumerate(zip(self.pins, self.offsets)):
            self.contacts.append(d[(string.ascii_uppercase.index(pin)+offset)%26])
        self.contacts = ''.join(self.contacts)

    def reorder_and_update_position(self, ptr):
        ptr.pins = ptr.reorder(ptr.pins, 1)
        ptr.contacts = ptr.reorder(ptr.contacts, 1)
        ptr.position = ptr.pins[0]
        ptr.previous_position = ptr.pins[-1]

    def key_press(self):
        """
        Rotates the necessary rotors prior to sending the key signal through the enigma machine.
        Points to note:
        If one rotor is on its notch, the next rotor along will rotate once along with the first.
        If the second rotor is on it's notch, it will rotate regardless of whether the first is.
        If the second rotor is one away from its notch, and the first is on its notch, the second rotor will rotate
        two times with two consecutive key presses aka "double step", which will subsequently turn the next rotor.
        If there is a fourth rotor, this never rotates.
        """
        #
        ptr=self
        # # Rotate rotor 1 and update positions
        self.reorder_and_update_position(ptr)

        # # Prior to rotating, if rotor 1 was on its notch...
        if ptr.notch == ptr.previous_position:
            ptr = ptr.left
            #...rotate the second rotor
            self.reorder_and_update_position(ptr)
            # If the second rotor was on its notch, also rotate the 3rd rotor
            if ptr.notch == ptr.previous_position:
                ptr=ptr.left
                self.reorder_and_update_position(ptr)
        # If rotor 1 wasn't on its notch...
        else:
            ptr = ptr.left
            #... but rotor 2 is, then rotate rotor 2
            if ptr.notch==ptr.position:
                self.reorder_and_update_position(ptr)
                #...and subsequently if rotor 3 is too, rotate 3
                if ptr.notch == ptr.previous_position:
                    ptr = ptr.left
                    self.reorder_and_update_position(ptr)

    def rotor_encode_left(self, input_index=0):
        self.output_char = self.contacts[input_index]
        self.output_index = self.pins.index(self.output_char)

    def rotor_encode_right(self, input_index=0):
        self.input_char = self.pins[input_index]
        self.output_index = self.contacts.index(self.input_char)
        self.output_char = self.pins[self.output_index]





