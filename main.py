from enigma import Enigma
import demonstrations, codebreak, codebreaker_tasks
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rotor_demo', default=None, action='store_true',
                        help='Run rotor demonstration tasks')
    parser.add_argument('--machine_demo', default=None, action='store_true',
                        help='Run machine demonstration tasks')
    parser.add_argument('--codebreaker', default=None, action='store_true',
                        help='Run all codebreaker tasks')
    parser.add_argument('--rotors', type=str, default='',
                        help='Choose 3 or 4 rotors i.e. "III II I" (space-delimited)')
    parser.add_argument('--reflector', type=str, default='', choices=['A', 'B', 'C'],
                        help="Choose reflector from A B or C")
    parser.add_argument('--ring_settings', type=str, default='',
                        help='Choose ring settings (1-26) for each rotor')
    parser.add_argument('--initial_positions', type=str, default='',
                        help='Choose initial positions for each rotor i.e. "A A B" (A-Z, space-delimited)')
    parser.add_argument('--plugboard_pairs', '-pbp', type=str, default='',
                        help='Choose up to 10 pairs of letters A-Z i.e. "AF BT LO PZ"')
    parser.add_argument('--code', type=str, default='',
                        help='Code to be run through Enigma')

    args = parser.parse_args()

    assert not ((args.rotor_demo or args.machine_demo) and
                ( args.rotors
                or args.reflector
                or args.ring_settings
                or args.initial_positions
                or args.plugboard_pairs)) \
        , 'Cannot call --rotor_demo or --machine_demo with other args'

    if not ((args.rotor_demo or args.machine_demo) or args.codebreaker):
        assert len(args.rotors.split()) == len(args.ring_settings.split()) == len(args.initial_positions.split()), \
            'Ensure rotors, ring settings and initial positions all have the same counts.'

        assert args.code, \
            'Manual mode: please use --code (str).'

    if args.plugboard_pairs:
        assert len(args.plugboard_pairs) <= 30, \
            'Too many plugboard pairs used, maximum is 10.'

    if args.code:
        assert not (' ' in args.code), \
            '--code contains a space. Enigma is not compatible with spaces, please correct.'

    return args


if __name__ == "__main__":

    args = get_args()
    if args.rotor_demo:
        demonstrations.rotor_demonstrations()

    elif args.machine_demo:
        demonstrations.machine_demonstrations()

    elif args.codebreaker:
        codebreaker_tasks.tasks()

    else:
        settings = {'rotors': args.rotors,
                    'reflector': args.reflector,
                    'ring_settings': args.ring_settings,
                    'initial_positions': args.initial_positions,
                    'plugboard_pairs': args.plugboard_pairs}
        e = Enigma(settings)
        e.create_machinery()
        e.encode(args.code)



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