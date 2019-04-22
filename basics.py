# region Algorithm's Introduction
def generaterandomstring(mask, bestmatchstring):
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    result = ""
    for i in range(len(mask)):
        char = ""
        if not mask[i]:
            char = alphabet[random.randrange(len(alphabet))]
        else:
            if bestmatchstring != "":
                char = bestmatchstring[i]
        result += char
    return result


class Match:
    def __init__(self, s=0, m=None):
        if m is None:
            m = []
        self.score = s
        self.mask = m


def matchscore(goalstring, teststring):
    count = 0
    mask = []
    for i in range(len(teststring)):
        if teststring[i] == goalstring[i]:
            mask.append(True)
            count += 1
        else:
            mask.append(False)
    score = float(count / len(teststring))
    return Match(score, mask)


# endregion
def main():
    goalstring = "me thinks it is like a weasel"
    stringmask = [False] * len(goalstring)
    newstring = ""
    loopmax = 10
    i = 0
    while True:
        newstring = generaterandomstring(stringmask, newstring)
        match = matchscore(goalstring, newstring)
        stringmask = match.mask
        if match.score == 1:
            break
        i += 1
        if i % loopmax == 0:
            print(i, newstring)
    print("done iterations= " + str(i))
