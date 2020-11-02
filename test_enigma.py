import pytest
from enigma import *
from plugboard import *


def test_raises_duplicatedplugs():
    # Test exception raised if the same character is used more than once in any pluglead pair
    plugboard = Plugboard()
    plugboard.add(PlugLead("SA"))

    with pytest.raises(Exception) as e:
        assert plugboard.add(PlugLead("SP"))


def test_raises_singlecharpluglead():
    # Test exception raised if only 1 character is entered for a pluglead
    plugboard = Plugboard()

    with pytest.raises(Exception) as e:
        assert plugboard.add(PlugLead("S"))


def test_rotordemo1():
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()

    output = e.encode('A')
    assert output == 'U'


def test_rotordemo2():
    # 2 A -> B
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('A')
    assert output == 'B'


def test_rotordemo3():
    # 3 A -> L
    settings = {'rotors': "I II III",
                'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'Q E V',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('A')
    assert output == 'L'


def test_rotordemo4():
    # 4 H -> Y
    settings = {'rotors': "IV V Beta",
                'reflector': 'B',
                'ring_settings': '14 9 24',
                'initial_positions': 'A A A',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('H')
    assert output == 'Y'


def test_rotordemo5():
    # 5 Z -> V
    settings = {'rotors': "I II III IV",
                'reflector': 'C',
                'ring_settings': '7 11 15 19',
                'initial_positions': 'Q E V Z',
                'plugboard_pairs': None}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('Z')
    assert output == 'V'


def test_machinedemo1():

    settings = {'rotors': "I II III", 'reflector': 'B',
                'ring_settings': '1 1 1',
                'initial_positions': 'A A Z',
                'plugboard_pairs': 'HL MO AJ CX BZ SR NI YW DG PK'}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('HELLOWORLD')
    assert output == 'RFKTMBXVVW'


def test_machinedemo2():
    settings = {'rotors': "IV V Beta I",
                'reflector': 'A',
                'ring_settings': '18 24 3 5',
                'initial_positions': 'E Z G P',
                'plugboard_pairs': 'PC XZ FM QA ST NB HY OR EV IU'}
    e = Enigma(settings)
    e.create_machinery()

    output=e.encode('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI')
    assert output == 'CONGRATULATIONSONPRODUCINGYOURWORKINGENIGMAMACHINESIMULATOR'
