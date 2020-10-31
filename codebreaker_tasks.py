from codebreak import CodeBreaker
import os

def tasks():
    """
    Contains the initial settings for each codebreaker task, and loads these settings into the Codebreaker class, then
    calls each respective task function. Outputs are saved to ./codebreak.txt
    """

    # Remove any existing codebreak text outputs
    if os.path.exists('./codebreak.txt'):
        os.remove('./codebreak.txt')

    # CODEBREAKER 1
    settings = {'code':'DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ',
                'crib': 'SECRETS',
                'rotors': 'Beta Gamma V',
                'reflector': 'UNKNOWN',
                'ring_settings': '04 02 14',
                'initial_positions':'M J M',
                'plugboard_pairs': 'KI XN FL'}
    e = CodeBreaker(settings)
    e.codebreak1_reflector()

    # CODEBREAKER 2
    settings = {'code':'CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH',
                'crib': 'UNIVERSITY',
                'rotors': 'Beta I III',
                'reflector': 'B',
                'ring_settings': '23 02 10',
                'initial_positions':'UNKNOWN',
                'plugboard_pairs': 'VH PT ZG BJ EY FS'}
    e = CodeBreaker(settings)
    e.codebreak2_positions()

    # CODEBREAKER 3
    settings = {'code':'ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY',
                'crib': 'THOUSANDS',
                'rotors': 'UNKNOWN',
                'reflector': 'UNKNOWN',
                'ring_settings': 'UNKNOWN',
                'initial_positions':'E M Y',
                'plugboard_pairs': 'FH TS BE UQ KD AL'}
    e = CodeBreaker(settings)
    e.codebreak3_multi()

    # CODEBREAKER 4
    settings = {'code': 'SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW',
                'crib':'TUTOR',
                'rotors':'V III IV',
                'reflector':'A',
                'ring_settings':'24 12 10',
                'initial_positions':'S W U',
                'plugboard_pairs': 'WP RJ A? VF I? HN CG BS'}
    e = CodeBreaker(settings)
    e.codebreak4_plugleads()

    # CODEBREAKER 5
    settings = {'code': 'HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX',
                'crib':['FACEBOOK','INSTAGRAM','TWITTER','SNAPCHAT','YOUTUBE','REDDIT','LINKEDIN'],
                'rotors':'V II IV',
                'reflector':'A',
                'ring_settings':'6 18 7',
                'initial_positions':'A J L',
                'plugboard_pairs': 'UG IE PO NX WT'}
    e = CodeBreaker(settings)
    e.codebreak5_rewiring()