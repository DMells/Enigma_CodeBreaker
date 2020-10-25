
class PlugLead:
    def __init__(self, mapping):

        self.mapping = mapping
        assert len(mapping) == 2, "Must be plugged into two letters"
        assert mapping[0] != mapping[1], "Cannot physically plug two identical letters"

    def encode(self, character):
        """
        Convert input character to it's associated encoded character via the plugboard
        input character : the character we want to encode

        return encoded_letter : the alternate letter
        """

        # If character not part of this particular leads mapping, encode the letter to itself
        if character not in self.mapping:
            encoded_letter = character
        else:
            # Else search for the index of the input character, and return the opposite
            encoded_letter = [self.mapping[1] if self.mapping.index(character)==0 else self.mapping[0]][0]
        print(f"Plugboard encoding -> {character} is plugged to {encoded_letter}")
        return encoded_letter


class Plugboard:
    def __init__(self):
        self.unusedplugleads = 10
        self.plugleads = []

    def add(self, pluglead):
        """
        Add instance of PlugLead to the PlugBoard (via plugleads list)
        1. Checks first if there are any unused plugleads
        2. Checks if any of the letters in the input string are already contained within
        another instance of PlugLead - if so returns ValueError
        3. Adds instance to plugleads list
        4. Reduces unusedplugleads by 1
        """
        if self.unusedplugleads > 0:
            if any(letter in pluglead.mapping for usedlead in self.plugleads for letter in usedlead.mapping):
                raise ValueError("Letter already used in another lead")

            self.plugleads.append(pluglead)
            self.unusedplugleads-=1
        else:
            raise ValueError("Lead creation exceeds max number of leads")

    def encode(self, character):
        """
        For the input character, loop through all instances of plugleads and find which one contains that character
        Return encoded character
        """

        # If no plugleads used, return original character
        if len(self.plugleads) == 0:
            return character
        else:
            encoded_char = character
            for lead in self.plugleads:
                # If the character exists in the mapping
                if character in lead.mapping:
                    # Encode the character
                    encoded_char = lead.encode(character)
                # Otherwise check the next pluglead
                else:
                    next
            return encoded_char


class individual_rotor:
    def __init__(self,name, rotor_box, ring_setting, position, left=None, right=None):
        self.name = name
        self.left = left
        self.right = right
        self.pins = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.contacts = rotor_box[name]['contacts']
        self.notch = rotor_box[name]['notch']
        self.rotatable = rotor_box[name]['rotatable']
        self.ring_setting = ring_setting
        self.position = position
        self.output_index = None
        self.encoded_char = None
        self.input_index = None

    def rotate(self, l, x):
        if self.rotatable:
            return l[x:] + l[:x]
        else:
            return l

    def adjust_starting_positions(self):
        # Adjust for starting position (rotates both pin and contact rings)
        print(f"Adjusting starting positions for {self.name}")
        num_position_rotations = ord('A') - ord(self.position)
        self.pins = self.rotate(self.pins, -num_position_rotations)
        self.contacts = self.rotate(self.contacts, -num_position_rotations)

        # Adjust for ring setting "-1" because ring_setting 1 is default
        self.contacts = self.rotate(self.contacts, -1 * (self.ring_setting-1))
        self.pins = self.rotate(self.pins, -1 * (self.ring_setting-1))

    def rotate_on_key_press(self):
        self.pins = self.rotate(self.pins, 1)
        self.contacts = self.rotate(self.contacts, 1)
        # Also update next left rotor if notch hit
        self.turnover()

    def rotor_encode_left(self, input_index):
        self.output_char = self.contacts[input_index]
        self.output_index = self.pins.index(self.output_char)
        print(f"Rotor {self.name}, Pin: {self.pins[input_index]}, "
              f"Pin is mapped internally to Contact {self.output_char}")

    def rotor_encode_right(self, input_index):
        self.input_char = self.pins[input_index]
        self.output_index = self.contacts.index(self.input_char)
        self.output_char = self.pins[self.output_index]
        # self.output_index = self.contacts.index(self.output_char)
        print(f"Rotor {self.name}, Contact: {self.input_char}, "
              f"Contact is mapped internally to Pin {self.output_char}")

    def turnover(self):
        if self.position == self.notch:
            print("Turnover triggered")
            nextrotor = self.left
            while True:
                # If there is a nextrotor
                if nextrotor is not None:
                    if nextrotor.position != nextrotor.notch:
                        nextrotor.pins = self.rotate(self.pins, 1)
                        nextrotor.contacts = self.rotate(self.contacts, 1)
                    else:
                        # double-step
                        nextrotor.pins = self.rotate(self.pins, 2)
                        nextrotor.contacts = self.rotate(self.contacts, 2)

                    nextrotor = nextrotor.left
                else:
                    break


class enigma_config:
    def __init__(self, board=None):
        self.root = None
        self.board = board
        self.rotor_box = {
         "Housing": {'contacts' :'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'notch': None, 'rotatable': False},
          "Beta": {'contacts':   'LEYJVCNIXWPBQMDRTAKZGFUHOS', 'notch': None, 'rotatable': True},
          "Gamma": {'contacts':  'FSOKANUERHMBTIYCWLQPZXVGJD', 'notch': None, 'rotatable': True},
          "I": {'contacts':      'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q', 'rotatable': True},
          "II": {'contacts':     'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E', 'rotatable': True},
          "III": {'contacts':    'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V', 'rotatable': True},
          "IV": {'contacts':     'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'notch': 'J', 'rotatable': True},
          "V": {'contacts':      'VZBRGITYUPSDNHLXAWMJQOFECK', 'notch': 'Z', 'rotatable': True},
          "A": {'contacts':      'EJMZALYXVBWFCRQUONTSPIKHGD', 'notch': None, 'rotatable': False},
          "B": {'contacts':      'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'notch': None, 'rotatable': False},
          "C": {'contacts':      'FVPJIAOYEDRZXWGCTKUQSBNMHL', 'notch': None, 'rotatable': False},
                          }

    def add(self, name, ring_setting=1, initial_position='A'):
        if self.root is None:
            self.root = individual_rotor(name, self.rotor_box, ring_setting, initial_position)
            self.root.adjust_starting_positions()
        else:
            ptr = self.root
            while True:
                if ptr.left is None:
                    ptr.left = individual_rotor(name, self.rotor_box, ring_setting, initial_position, right=ptr)
                    ptr.left.adjust_starting_positions()
                    break
                else:
                    ptr = ptr.left

    def encode(self, phrase):
        """
        If input 'A'
        1. Rotate first rotor one position - do we actually alter the list itself or just maintain a counter? Probably a counter, but will have to track when it
        reaches 26 to make sure it gets reset

        """
        print("Begin encode")
        i=0

        encoded_phrase = []

        # For each character in the phrase
        while i < len(phrase):
            # New character, therefore reset ptr to root (housing)
            character = phrase[i]
            if self.board:
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
            print("Reflector hit")
            ptr = ptr.right
            while True:
                if ptr.right:
                    # if ptr.left.name in ['A','B','C']:
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
            print(encoded_phrase)


if __name__ == "__main__":
    # You can use this section to write tests and demonstrations of your enigma code.
    board = Plugboard()
    board.add(PlugLead("HL"))
    board.add(PlugLead("MO"))
    board.add(PlugLead("AJ"))
    board.add(PlugLead("CX"))
    board.add(PlugLead("BZ"))
    board.add(PlugLead("SR"))
    board.add(PlugLead("NI"))
    board.add(PlugLead("YW"))
    board.add(PlugLead("DG"))
    board.add(PlugLead("PK"))
    print(board.encode(""))

    c = enigma_config(board)
    c.add("Housing")
    c.add("III",ring_setting=1, initial_position='Z')
    c.add("II",ring_setting=1, initial_position='A')
    c.add("I", ring_setting=1, initial_position='A')
    c.add("B")
    c.encode("HELLOWORLD")

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