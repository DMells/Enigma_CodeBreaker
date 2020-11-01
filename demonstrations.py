from enigma import Enigma

def rotor_demonstrations():
    # MULTIPLE ROTOR DEMONSTRATION

    # 1 A -> U
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    print("******Demo 1******\n")
    e.encode('A')
    print('\n\n')

    # 2 A -> B
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    print("******Demo 2******\n")
    e.encode('A')
    print('\n\n')

    # 3 A -> L
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'Q E V',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    print("******Demo 3******\n")
    e.encode('A')
    print('\n\n')
    # 4 H -> Y
    settings = {'rotors': "IV V Beta",
                'reflector': 'B',
                'ring_settings': '14 9 24',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    print("******Demo 4******\n")
    e.encode('H')
    print('\n\n')
    # 5 Z -> V
    settings = {'rotors': "I II III IV",
                'reflector': 'C',
                'ring_settings': '7 11 15 19',
                'initial_positions': 'Q E V Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()
    print("******Demo 5******\n")
    e.encode('Z')
    print('\n\n')


def machine_demonstrations():

    settings = {'rotors': "I II III", 'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': 'HL MO AJ CX BZ SR NI YW DG PK'}
    e = Enigma(settings)
    e.create_machinery()
    print("******Machine Example 1******\n")
    e.encode('HELLOWORLD')
    print('\n\n')

    settings = {'rotors': "IV V Beta I",
                'reflector': 'A',
                'ring_settings': '18 24 3 5',
                'initial_positions': 'E Z G P',
                'plugboard_pairs': 'PC XZ FM QA ST NB HY OR EV IU'}
    e = Enigma(settings)
    e.create_machinery()
    print("******Machine Example 2******\n")
    e.encode('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI')
    print('\n\n')