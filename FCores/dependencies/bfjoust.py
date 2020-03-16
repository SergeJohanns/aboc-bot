# BF Joust interpreter
from typing import Dict, List, Tuple, Union

MAX_CYCLES = 100000

def run_fight(warrior_1: str, warrior_2: str) -> Tuple[int, int]:
    result = sum(duel(i, warrior_1, warrior_2, polswitch=False) + duel(i, warrior_1, warrior_2, polswitch=True) for i in range(10, 31))
    return (result, -result)

def duel(tape_length, warrior_1: str, warrior_2: str, polswitch=False) -> int:
    warrior = [warrior_1, warrior_2]
    tape = [128] + [0 for _ in range(tape_length - 2)] + [128]
    state = [{"ptr":0, "codeptr":0, "movepol":1, "pol":1}, {"ptr":(tape_length - 1), "codeptr":0, "movepol":-1, "pol":(0 if polswitch else 1)}]
    flagged = [False, False]
    lost = [False, False]
    for _ in range(MAX_CYCLES):
        move = [step(tape, warrior[player], state[player]) for player in range(2)]
        for player in range(2):
            make_move(tape, move[player], state[player])
        for player in range(2):
            flag = tape[0] == 0
            lost[player] = (flag and flagged[player]) or state[player]["ptr"] < 0 or state[player]["ptr"] >= tape_length
            flagged[player] = flag
        if any(lost):
            return lost[1] - lost[0] # -1, 0, or 1 if 2 won, it was a draw, or 1 won, respectively.
    return 0

def make_move(tape: List[int], move: str, state: Dict[str, int]):
    if move == '+':
        tape[state["ptr"]] += state["pol"]
    elif move == '-':
        tape[state["ptr"]] -= state["pol"]

def step(tape: List[int], code: str, state: Dict[str, int]) -> Union[str, None]:
    jump = False
    jumpdir = 1
    jumpdepth = 0
    while state["codeptr"] < len(code):
        curr = code[state["codeptr"]]
        state["codeptr"] += 1 # Preemtively increment the pointer, since there is only one case in which it shouldn't be.
        if jump:
            if curr == '[':
                jumpdepth += 1
            elif curr == ']':
                jumpdepth -= 1
            if jumpdepth:
                state["codeptr"] += jumpdir - 1 # Undo the preemtive increment and then change in the direction.
            else:
                jump = False
                return None # At the end of the jump the command is considered complete.
        elif (curr == '[' and (cell := tape[state["ptr"]]) == 0) or (curr == ']' and cell != 0):
            jump = True
            jumpdir = 1 if curr == '[' else -1
            jumpdepth = 1 if curr == '[' else -1
        elif curr == '>':
            state["ptr"] += state["movepol"]
            return None
        elif curr == '<':
            state["ptr"] -= state["movepol"]
            return None
        elif curr == '+' or curr == '-':
            return curr
    return None