# Finite State Machine (FSM) Processor

## Introduction
The Finite State Machine (FSM) Processor is a Python script designed for the creation and manipulation of Non-Deterministic Finite Automata (NFA) and their conversion to Deterministic Finite Automata (DFA). This utility is capable of processing regular expressions by constructing an equivalent NFA, performing operations such as union, concatenation, and Kleene star, and then converting the NFA into a DFA. Additionally, the script can evaluate whether a given string is accepted by the NFA.

## Features
- **NFA Creation**: Generate NFAs for individual characters.
- **Concatenation**: Combine two NFAs to create a new NFA that recognizes the concatenation of their languages.
- **Union**: Create a new NFA that recognizes the union of the languages of two NFAs.
- **Kleene Star**: Apply the Kleene star operation to an NFA to recognize the Kleene closure of its language.
- **ε-Closure Computation**: Determine the set of states reachable from a given set of states on ε-transitions alone.
- **Transition on Character**: Compute the set of states the NFA moves to on a given input character.
- **NFA to DFA Conversion**: Transform an NFA into an equivalent DFA.
- **String Acceptance**: Check if a string is accepted by the NFA.

## Requirements
- Python 3.x
- No external libraries are needed for the core functionality.

## Setup
1. Ensure Python 3.x is installed on your machine.
2. Clone this repository or download the script directly.
3. The script is self-contained and does not require additional setup.

## Usage
To utilize the script, import the `Fsm` class and other functions within a Python environment or another script. Here is a basic example of using the script to create an NFA for a character and check a string acceptance:

```python
from fsm_processor import char, accept

# Create an NFA for character 'a'
nfa = char('a')

# Check if the string 'a' is accepted by the NFA
is_accepted = accept(nfa, 'a')
print(f"The string 'a' is {'accepted' if is_accepted else 'not accepted'} by the NFA.")
