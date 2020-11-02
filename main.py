from enigma import Enigma
import demonstrations, codebreaker_tasks
import argparse


def get_args():
    """
    Obtain arguments as specified by the user input and parse them
    return args: parsed arguments
    """
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
        assert len(args.rotors.split(' ')) <= 4, 'Too many rotors added, choose 3 or 4'
        assert len(args.rotors.split(' ')) >= 3, 'Too few rotors added, choose 3 or 4'
        assert args.code, 'Manual mode: please use --code (str).'

    if args.plugboard_pairs:
        assert len(args.plugboard_pairs) <= 30, 'Too many plugboard pairs used, maximum is 10.'

    if args.code:
        assert not (' ' in args.code), '--code contains a space. Enigma is not compatible with spaces, please correct.'

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