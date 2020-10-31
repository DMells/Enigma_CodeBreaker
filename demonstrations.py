from enigma import Enigma

def run_demonstrations():
    # MULTIPLE ROTOR DEMONSTRATION

    # 1 A -> U
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('A')

    # 2 A -> B
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('A')

    # 3 A -> L
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'Q E V',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('A')

    # 4 H -> Y
    settings = {'rotors': "IV V Beta",
                'reflector': 'B',
                'ring_settings': '14 9 24',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('H')

    # 5 Z -> V
    settings = {'rotors': "I II III IV",
                'reflector': 'C',
                'ring_settings': '7 11 15 19',
                'initial_positions': 'Q E V Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('Z')

    #######################
    ##### EXAMPLE 1 #######
    #######################
    settings = {'rotors': "I II III", 'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': 'HL MO AJ CX BZ SR NI YW DG PK'}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('HELLOWORLD')

    #######################
    ##### EXAMPLE 2 #######
    #######################
    settings = {'rotors': "IV V Beta I",
                'reflector': 'A',
                'ring_settings': '18 24 3 5',
                'initial_positions': 'E Z G P',
                'plugboard_pairs': 'PC XZ FM QA ST NB HY OR EV IU'}
    e = Enigma(settings)
    e.create_machinery()
    e.encode('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI')