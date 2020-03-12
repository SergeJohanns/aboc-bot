# BF Joust interpreter
import itertools
from typing import Dict, List, Tuple, Union

MAX_CYCLES = 100000

def run_fight(warrior_1: str, warrior_2: str) -> Tuple[int, int]:
    res_1 = 0
    res_2 = 0
    scores = itertools.chain(*((duel(i, warrior_1, warrior_2, polswitch=False), duel(i, warrior_1, warrior_2, polswitch=True)) for i in range(10, 31)))
    for score in scores:
        res_1 += score
        res_2 -= score
    return (res_1, res_2)

def duel(tape_length, warrior_1: str, warrior_2: str, polswitch=False) -> int:
    tape = [128] + [0 for _ in range(tape_length - 2)] + [128]
    state_1 = {"ptr":0, "codeptr":0, "movepol":1, "pol":1}
    state_2 = {"ptr":(tape_length - 1), "codeptr":0, "movepol":-1, "pol":(0 if polswitch else 1)}
    flagged_1 = False
    flagged_2 = False
    lost_1 = False
    lost_2 = False
    for _ in range(MAX_CYCLES):
        move_1 = step(tape, warrior_1, state_1)
        move_2 = step(tape, warrior_2, state_2)
        make_move(tape, move_1, state_1)
        make_move(tape, move_2, state_2)
        flag_1 = tape[0] == 0
        flag_2 = tape[-1] == 0
        if (flag_1 and flagged_1) or state_1["ptr"] < 0 or state_1["ptr"] >= tape_length:
            lost_1 = True
        if (flag_2 and flagged_2) or state_2["ptr"] < 0 or state_2["ptr"] >= tape_length:
            lost_2 = True
        if lost_1 and lost_2:
            return 0
        elif lost_2:
            return 1
        elif lost_1:
            return -1
        flagged_1 = flag_1
        flagged_2 = flag_2
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
        if jump:
            if curr == '[':
                jumpdepth += 1
            elif curr == ']':
                jumpdepth -= 1
            if jumpdepth:
                state["codeptr"] += jumpdir
            else:
                jump = False
                state["codeptr"] += 1
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