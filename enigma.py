from plugboard import PlugBoard
import string

class Rotor:
    def __init__(self,name, rotor_box, ring_setting, position, rotor_num, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right
        self.rotor_num = rotor_num
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
        if self.name not in ['A','B','C']:
            # print(f"Adjusting starting positions for {self.name}")
            num_position_rotations = (string.ascii_uppercase.index('A') + string.ascii_uppercase.index(self.position)) % 26
            self.pins = self.rotate(self.pins, num_position_rotations)
            self.contacts = self.rotate(self.contacts, num_position_rotations)


    def adjust_ring_setting(self):
        # Get initial offsets
        self.offsets = []
        for (pin, contact) in zip(self.pins, self.contacts):
            self.offsets.append(string.ascii_uppercase.index(contact) - string.ascii_uppercase.index(pin))

        self.offsets = self.rotate(self.offsets, -1 * (self.ring_setting-1))
        self.old_contacts = self.contacts
        self.contacts = []
        d = dict(enumerate(string.ascii_uppercase, 0))
        for i, (pin, offset) in enumerate(zip(self.pins, self.offsets)):
            self.contacts.append(d[(string.ascii_uppercase.index(pin)+offset)%26])
        self.contacts = ''.join(self.contacts)

    def rotate_on_key_press(self):
        # Rotate first rotor, update current position
        self.pins = self.rotate(self.pins, 1)
        self.contacts = self.rotate(self.contacts, 1)
        self.position = self.pins[0]
        self.previous_position = self.pins[-1]
        self.left.previous_position = self.pins[0]

        if self.notch == self.previous_position:
            self.left.pins = self.rotate(self.left.pins, 1)
            self.left.contacts = self.rotate(self.left.contacts, 1)
            self.left.position = self.left.pins[0]
            self.left.previous_position = self.left.pins[-1]

            # If next rotor is on its notch, rotate position
            if self.left.previous_position == self.left.notch:
                # self.left.pins = self.rotate(self.left.pins, 1)
                # self.left.contacts = self.rotate(self.left.contacts, 1)
                # self.left.position = self.left.pins[0]
                # self.left.previous_position = self.left.pins[-1]

                self.left.left.pins = self.rotate(self.left.left.pins, 1)
                self.left.left.contacts = self.rotate(self.left.left.contacts, 1)
                self.left.left.position = self.left.left.pins[0]
                self.left.left.previous_position = self.left.left.pins[-1]
        else:
            if self.left.position == self.left.notch:
                self.left.pins = self.rotate(self.left.pins, 1)
                self.left.contacts = self.rotate(self.left.contacts, 1)
                self.left.position = self.left.pins[0]
                self.left.previous_position = self.left.pins[-1]

                if self.left.previous_position == self.left.notch:
                    self.left.left.pins = self.rotate(self.left.left.pins, 1)
                    self.left.left.contacts = self.rotate(self.left.left.contacts, 1)
                    self.left.left.position = self.left.left.pins[0]
                    self.left.left.previous_position = self.left.left.pins[-1]

        # if self.notch:
        #     # Also update next left rotor if notch hit
        #     self.turnover()

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

        # self.create_machinery()

    def create_machinery(self):
        # Add plugboard
        self.board = PlugBoard(self.settings)
        # Add housing
        self.add("Housing")
        # Add rotors
        for i in range(len(self.settings['rotors'].split(' '))-1,-1, -1):
            rotor_num = 1
            rotor_name = self.settings['rotors'].split(' ')[i]
            ring_setting = self.settings['ring_settings'].split(' ')[i]
            initial_position = self.settings['initial_positions'].split(' ')[i]
            self.add(rotor_name,rotor_num, ring_setting, initial_position)
            rotor_num +=1
        # Add reflector
        self.add(self.settings['reflector'])

    def add(self, name, rotor_num=None, ring_setting=1, initial_position='A'):
        if self.root is None:
            self.root = Rotor(name, self.rotor_box, ring_setting, initial_position, rotor_num)
            self.root.adjust_ring_setting()
            self.root.adjust_starting_positions()
        else:
            ptr = self.root
            while True:
                if ptr.left is None:

                    ptr.left = Rotor(name, self.rotor_box, ring_setting, initial_position, rotor_num, right=ptr)
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
        try:
            print(
                f'Final Rotor Positions:{self.root.left.left.left.left.position}{self.root.left.left.left.position}{self.root.left.left.position}{self.root.left.position}')
        except:
            print(f'Final Rotor Positions:{self.root.left.left.left.position}{self.root.left.left.position}{self.root.left.position}')
        return ''.join(encoded_phrase)


