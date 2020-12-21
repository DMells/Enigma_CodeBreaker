# Enigma Codebreaker Challenge
This piece was submitted as part of an Object Oriented Programming exercise for the Artificial Intelligence MSc (Bath University)

The project is split into two parts:
1. Construction of the Enigma machine (simulation to mimic the mechanics used by the Enigma machine used in WWII) with subsequent tests
2. Codebreaker challenges where specific parts of the machine "went missing" and workarounds must be found

<i>The actual assignment is detailed in `enigma.ipynb` if you wish to replicate.</i>

##How it works
The machine itself is broken into several key concepts:
- A plugboard, where a letter is directly mapped to another. Functionality includes adding user-defined plugleads to the plugboard
- The rotors - there is a choice of 7 rotors, each containing a set of "pins" and "contacts" used to map one letter to another. The rotors are designed to rotate upon each key press, and the initial configuration of the rotor consists of the starting position of the rotor itself and the internal mappings for the letters.
- The reflector - A direct one-to-one mapping to another letter which will then be "reflected" back through the rotors.
)

Upon "key press" the rotators all rotate once (or more than once if the rotor is on it's "notch") and the signal works it's way through the rotors, hits the reflector, and then back through the rotors to give and encrypted letter. The process then repeats until the full input string has been encrypted.

### Operating Instructions
For a quick sample of pre-configured settings and messages:
`python main.py --machine_demo`

For a customised input and machine set up, use additional arguments i.e:
```
python main.py --
--rotors
"III II I"
--reflector
"B"
--ring_settings
"1 1 1"
--initial_positions
"Y D Q"
--code
"AAAA"
```
Please review the `get_args()` function in `main.py` for details of available rotors (etc)