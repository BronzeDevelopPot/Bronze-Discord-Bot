import random 

def RSP():
    r = random.randrange(1, 4)
    if r == 1:
        return "가위"
    elif r == 2:
        return "바위"
    elif r == 3:
        return "보"

