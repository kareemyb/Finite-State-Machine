import re
from functools import reduce

class Fsm:
  def __init__(self,alphabet,states,start,final,transitions):
    self.sigma = alphabet
    self.states = states
    self.start = start
    self.final = final
    self.transitions = transitions
  def __str__(self):
    sigma = "Alphabet: " + str(self.sigma) + "\n"
    states = "States: " + str(self.states) + "\n"
    start = "Start: " + str(self.start) + "\n"
    final = "Final: " + str(self.final) + "\n"
    trans_header = "Transitions: [\n"
    thlen = len(trans_header)
    translist = ""
    for t in self.transitions:
      translist += " " * thlen + str(t)+ "\n"
    translist += " " * thlen + "]"
    transitions = trans_header + translist
    ret = sigma + states + start + final + transitions 
    return ret

count = 0

def fresh(): 
  global count
  count += 1
  return count

'''
Function converts a character into an NFA (FSM object)
'''
def char(string):
  # Generating unique state numbers
  start_state = fresh()
  accept_state = fresh()

  # Creating new NFA that only recognizes the provided characters
  return Fsm([string], [start_state, accept_state], start_state, [accept_state], [(start_state, string, accept_state)])

'''
Function returns a concatenation of two NFAs
'''
def concat(r1,r2):
  # Creating epsilon transitions from each of the accepting states of r1 to the start state of r2
  epsilon_transitions = [(state, 'epsilon', r2.start) for state in r1.final]

  # Transitions for concatenated NFA is the union of transitions of r1 and r2, along with newly created epsilon transitions
  transitions = r1.transitions + r2.transitions + epsilon_transitions

  # States of concatenated NFA is the union of states of r1 and r2
  states = r1.states + r2.states

  # Starting state of concatenated NFA is just starting state of r1
  starting_state = r1.start

  # Accepting states of concatenated NFA are just the accepting states of r2
  accepting_states = r2.final

  # CAN I CONCATENATE THE SIGMAS (ALPHABETS/CHARACTERS) INTO A SET (TO AVOID REPEATS) THEN PASS IT INSTEAD
  return Fsm(r1.sigma + r2.sigma, states, starting_state, accepting_states, transitions)

'''
Function returns a union of two NFAs
'''
def union(r1,r2):
  # Creating fresh state start state
  new_start = fresh()

  # Creating epsilon transitions from new start state to start states of r1 and r2
  epsilon_transitions = [(new_start, 'epsilon', r1.start), (new_start, 'epsilon', r2.start)]

  # Transitions for resulting NFA are the union of transitions of r1 and r2, along with newly created epsilon transitions
  transitions = r1.transitions + r2.transitions + epsilon_transitions

  # States of resulting NFA are union of the states of r1 and r2, along with new start state
  states = [new_start] + r1.states + r2.states

  # Accepting states of resulting NFA are union of accepting states of r1 and r2
  accepting_states = r1.final + r2.final

  return Fsm(r1.sigma + r2.sigma, states, new_start, accepting_states, transitions)


'''
Function returns NFA that has Kleene Closure applied to it
'''
def star(r1):
  # Instantiating new start state, which will also be an accepting state
  new_start = fresh()

  # Creating epsilon transtions from new start state to start state of the NFA
  # and from each of the accepting states of the NFA back to its start state
  epsilon_transitions = [(new_start, 'epsilon', r1.start)] + [(state, 'epsilon', r1.start) for state in r1.final]

  # Transitions for resulting NFA are transitions of original NFA and newly created epsilon transitions
  transitions = r1.transitions + epsilon_transitions

  # States of resulting NFA are states of original NFA and new start state
  states = [new_start] + r1.states

  # Start state of resulting NFA is new start state
  start = new_start

  # Accepting states of resulting NFA are accepting states of original NFA, along with new start state
  accepting_states = [new_start] + r1.final

  return Fsm(r1.sigma, states, start, accepting_states, transitions)
  
'''
Function outputs possible set of states (list) of NFA after zero or more
epsilon transitions after starting from initial state
''' 
def e_closure(s,nfa):
  # Instantiating result set with the intial states
  result = set(s)

  # Initializing worklist with the initial states
  worklist = list(s)

  # Looping while there are states to process
  while worklist:
    # Retrieving last element from worklist
    state = worklist.pop()

    # Check for any epsilong transitions from this state
    for transition in nfa.transitions:
      # Unpacking and assigning elements from transition
      src, letter, destination = transition
      if src == state and letter == 'epsilon':
        if destination not in result:
          result.add(destination)
          worklist.append(destination)

  return list(result) 

'''
Function outputs set of possible states (list) that NFA might be in after one
transition from the start
''' 
def move(c,s,nfa):
  # Checking if the symbol c is in the NFA's alphabet
  if c not in nfa.sigma and c != 'epsilon':
    return []
  
  # Initializing empty set to store result
  result = set()

  for state in s:
    for transition in nfa.transitions:
      # Unpacking and assigning elements from transition
      src, letter, destination = transition
      if src == state and letter == c:
        result.add(destination)
  
  # Transforming and returning set as a list
  return list(result)
      

'''
Function converts an NFA to a DFA
'''
def nfa_to_dfa(nfa): 
  # Instantiate the start state of the DFA using the epsilon closure of the NFA's start state
  dfa_start = tuple(e_closure([nfa.start], nfa))

  # List of DFA states to be processed (each state is a set of NFA states)
  unprocessed_dfa = [dfa_start]

  # List of processed DFA states
  processed_dfa = []

  # List of DFA Transitions
  transitions_dfa = []

  while unprocessed_dfa:
    # Retrieving last state of unprocessed states
    current_dfa_state = unprocessed_dfa.pop()

    # Moving state to processed states
    processed_dfa.append(current_dfa_state)

    # Computing the DFA transition for each character (sigma) of the NFA's alphabet
    for character in nfa.sigma:
      # Finding set of reachable NFA states from current DFA states
      moved_states = move(character, current_dfa_state, nfa)

      # Computing epsilon closure to get the corresponding DFA state
      next_dfa_state = tuple(e_closure(moved_states, nfa))

      # Add transition to dfa_transitions
      transitions_dfa.append((current_dfa_state, character, next_dfa_state))

      # Add the DFA state to unprocessed states if it hasn't been seen already
      if next_dfa_state not in processed_dfa and next_dfa_state not in unprocessed_dfa:
        unprocessed_dfa.append(next_dfa_state)

  # Determine the final states for the DFA
  dfa_final = [state for state in processed_dfa if any(nfa_state in nfa.final for nfa_state in state)]

  # Create and return the DFA
  return Fsm(nfa.sigma, processed_dfa, dfa_start, dfa_final, transitions_dfa)



'''
Function takes NFA and string and returns whehter NFA accepts the string
'''
def accept(nfa,string):
  # Getting epsilon closure of start state
  current_states = e_closure([nfa.start], nfa)

  # Processing each character in the string
  for char in string:
    # Find the set of states to transition this character
    moved_states = move(char, current_states, nfa)
    # Compute the epsilon closure of this set
    current_states = e_closure(moved_states, nfa)

  # Check if any of the states in the final set is an accepting state
  for state in current_states:
    if state in nfa.final:
      return True
  return False
