# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", # A -> E, B -> K, C -> M. 이친구의 노치는 16번에 있다
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE", # A -> A, B -> J, C -> D. K에서 S로 이동시 회전
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO", # A -> B, B -> D, C -> F. K에서 M으로 이동시 회전 
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard): #입력값 할당
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    # reverse = false일때 왼쪽 -> 오른쪽 순서로 읽음.
    if reverse :
        for j in range(0,3) :
            for i in range(0,26) :
                if input == SETTINGS["WHEELS"][j]["wire"][(i + SETTINGS["WHEEL_POS"][j]) % 26] :
                    input = chr(ord('A') + i)
                    break

    else :
        input = SETTINGS["WHEELS"][2]["wire"][(ord(input) + SETTINGS["WHEEL_POS"][2] - ord('A')) % 26]
        input = SETTINGS["WHEELS"][1]["wire"][(ord(input) + SETTINGS["WHEEL_POS"][1] - ord('A')) % 26]
        input = SETTINGS["WHEELS"][0]["wire"][(ord(input) + SETTINGS["WHEEL_POS"][0] - ord('A')) % 26]
    
    return input

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    # 글자 입력할때마다 한번씩 돎.
    # 각 wheel마다 notch가 존재. 해당 turn index에 해당하는 알파벳이 catch에 설정된 상태로 글자를 입력하게 되면, 다음 로터가 돌게 됨.
    SETTINGS["WHEEL_POS"][2] = (SETTINGS["WHEEL_POS"][2] + 1) % 26

    if SETTINGS["WHEEL_POS"][2] == SETTINGS["WHEELS"][2]["turn"]:
        SETTINGS["WHEEL_POS"][1] == (SETTINGS["WHEEL_POS"][1] + 1) % 26
    if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]["turn"]:
        SETTINGS["WHEEL_POS"][0] == (SETTINGS["WHEEL_POS"][0] + 1) % 26
    pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
