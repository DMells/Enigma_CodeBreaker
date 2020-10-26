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
    def __init__(self, settings):
        self.unusedplugleads = 10
        self.plugleads = []
        self.pairs = settings['plugboard_pairs']

        if self.pairs:
            self.create_plugboard()

    def create_plugboard(self):
        for i in self.pairs.split(' '):
            self.add(PlugLead(i))

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