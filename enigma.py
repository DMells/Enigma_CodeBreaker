from plugboard import Plugboard
import string
from abc import abstractmethod

class Enigma:
    """
    The core class for the Enigma machine. Takes in a settings dictionary as provided by the user, and constructs the
    required machine from the settings blueprints. The structure of the machine is as follows:
    1. Plugboard with required plugleads
    2. Housing - a simple list from A-Z, never rotates
    3. Rotors - 3 or 4 with respective pins and contacts, these rotate with each 'key press'
    4. 1 Reflector - which will map the final rotor output to a different letter before passing the signal rightwards.
    """
    def __init__(self, settings:dict):
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
        """
        Adds in turn each part of the machine as specified in the user settings.
        """

        # Add plugboard with respective pluglead pairs
        self.board = Plugboard(self.settings)
        # Add housing
        self.add("Housing")
        # Add rotors. Rotors are 'inserted' in reverse order from right to left
        for i in range(len(self.settings['rotors'].split(' '))-1,-1, -1):
            rotor_name = self.settings['rotors'].split(' ')[i]
            ring_setting = self.settings['ring_settings'].split(' ')[i]
            initial_position = self.settings['initial_positions'].split(' ')[i]
            self.add(rotor_name, ring_setting, initial_position)

        # Add reflector
        self.add(self.settings['reflector'])

    @abstractmethod
    def add(self, name:str, ring_setting:int = 1, initial_position:str = 'A'):
        """
        Adds a named mechanical part to the machine from right to left, and then adjusts the default part setting
        to reflect the desired ring setting and initial position

        :param name: Name of the part being added (see self.rotor_box in the __init__ method for details)
        :param ring_setting: An integer from 1-26 determining the pin-to-contact mapping for the rotor
        :param initial_position: The starting position for the rotor
        """
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

    def encode(self, message:str) -> str:
        """
        Takes the users input message and runs each character through the enigma machine from right to left, and back
        again, to produce an encoded character. Encoded characters are combined into a single list and returned/printed
        as one encoded/decoded message.

        :param message: The message to be decoded/encoded
        :return: decoded/encoded message string
        """
        i=0
        encoded_phrase = []
        # For each character in the message
        while i < len(message):
            character = message[i]
            # Run the character through the plugboard
            character = self.board.encode(character)

            ptr = self.root
            # Rotate all rotors as necessary
            ptr.left.key_press()

            # Assign the Housing (first "ptr.contacts") index of the character to input_index inside the first rotor object
            ptr.left.input_index = ptr.contacts.index(character.upper())
            ptr = ptr.left

            while True:
                # If there is another rotor to the left
                if ptr.left is not None:
                    # If Housing is to the right of the current rotor...
                    if ptr.right.name == 'Housing':
                    # ..pass the Housing/input index to the first rotor pins, to get the associated contact/output index
                        ptr.rotor_encode_left(ptr.input_index)
                    else:
                        # Else if it is a rotor to the right, grab that rotors encoded/output character
                        ptr.rotor_encode_left(ptr.right.output_index)
                    # Set pointer to the next part to the left and repeat
                    ptr = ptr.left
                else:
                    # No more rotors, now run signal through the reflector
                    ptr.rotor_encode_left(ptr.right.output_index)
                    break

            # Pass signal from reflector back through to the plugboard
            ptr = ptr.right
            while True:
                if ptr.right:
                    # If there is another machine element to the right position, encode as normal
                    ptr.rotor_encode_right(ptr.left.output_index)
                    ptr = ptr.right
                else:
                    # If there are no more parts to pass the signal through, encode, run through the plugboard if it
                    # exists, then append the output to the output phrase list
                    ptr.rotor_encode_right(ptr.left.output_index)
                    if self.board:
                        ptr.output_char = self.board.encode(ptr.output_char)
                    encoded_phrase.append(ptr.output_char)
                    break
            # Increase i by one to then loop back and start again for the next character
            i+=1

        print(f"Input Phrase: {message}")
        print(f"Encoded Phrase: {''.join(encoded_phrase)}")

        if len(self.settings['rotors'].split(' ')) == 3:
            print(
                f'Final Rotor Positions:{self.root.left.left.left.position}'
                f'{self.root.left.left.position}'
                f'{self.root.left.position}')
        else:
            print(f'Final Rotor Positions:{self.root.left.left.left.left.position}'
                  f'{self.root.left.left.left.position}'
                  f'{self.root.left.left.position}'
                  f'{self.root.left.position}')

        return ''.join(encoded_phrase)


class Rotor(Enigma):
    """
    The rotor class (also used by reflector and housing parts) contains the methods for adjusting starting positions and ring settings,
    rotating the rotors on key press, and encoding left and right
    """
    def __init__(self,name: str, rotor_box, ring_setting: int = 1, position: str = 'A', left: object = None,
                 right: object = None):
        super().__init__(rotor_box)
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

    @abstractmethod
    def reorder(self, l: [], x: int):
        '''Rotates a list by slicing at the given index and swapping the two parts around'''
        return l[x:] + l[:x]

    def adjust_starting_positions(self):
        '''Adjusts the rotor for starting position (rotates both pin and contact rings) as per user settings'''

        # If the current pointer is not a reflector
        if self.name not in ['A','B','C']:
            # Get the number of rotations required to put the rotor at the desired starting position
            num_position_rotations = (string.ascii_uppercase.index('A') + string.ascii_uppercase.index(self.position))\
                                     % 26
            # Rotate both pins and contacts in unison
            self.pins = self.reorder(self.pins, num_position_rotations)
            self.contacts = self.reorder(self.contacts, num_position_rotations)

    def adjust_ring_setting(self):
        ''' Adjusts the rotor for the user-defined ring setting by altering the mappings from pins to contacts '''

        self.offsets = []
        # For each pin-contact pair, create a list noting the numerical (levenshtein) distance between them
        for (pin, contact) in zip(self.pins, self.contacts):
            self.offsets.append(string.ascii_uppercase.index(contact) - string.ascii_uppercase.index(pin))

        # Rotate the list of numerical distances (mappings) as determined by the ring setting
        self.offsets = self.reorder(self.offsets, -1 * (self.ring_setting - 1))
        self.contacts = []

        # Create an enumerated dictionary of all the uppercase letters A-Z
        enum_alpha = dict(enumerate(string.ascii_uppercase, 0))

        # Recreate the new contacts list by mapping the pin index plus the offset to the value of the enumerated dict
        for (pin, offset) in zip(self.pins, self.offsets):
            self.contacts.append(enum_alpha[(string.ascii_uppercase.index(pin)+offset)%26])
        self.contacts = ''.join(self.contacts)

    @abstractmethod
    def reorder_and_update_position(self, ptr: object):
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

    def rotor_encode_left(self, input_index: int = 0):
        """Passes the signal leftwards (pin->contact) through the current machine part to get the
        next encoded character"""

        # Use the previous machine parts pin/output index (or if the first rotor, the Housing index) to get
        # the associated contact letter
        self.output_char = self.contacts[input_index]
        # Use that contact letter to get the index of that letter in the pins list
        self.output_index = self.pins.index(self.output_char)

    def rotor_encode_right(self, input_index: int = 0):
        """Passes the signal rightwards (contact->pin) through the current machine part"""

        self.input_char = self.pins[input_index]
        self.output_index = self.contacts.index(self.input_char)
        self.output_char = self.pins[self.output_index]





