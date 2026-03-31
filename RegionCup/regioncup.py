import telebot
import threading
import keys
import time
import shutil

groupId = keys.ID
bot = telebot.TeleBot(keys.TOKEN)

teams = [
    ('Team 1', 'Full name team 1', 'Toto team 1 1', 'Toto team 1 2', 'Toto team 1 3'),
    ('Team 2', 'Full name team 2', 'Toto team 2 1', 'Toto team 2 2', 'Toto team 2 3'),
    ('Team 3', 'Full name team 3', 'Toto team 3 1', 'Toto team 3 2', 'Toto team 3 3'),
    ('Team 4', 'Full name team 4', 'Toto team 4 1', 'Toto team 4 2', 'Toto team 4 3'),
    ('Team 5', 'Full name team 5', 'Toto team 5 1', 'Toto team 5 2', 'Toto team 5 3'),
    ('Team 6', 'Full name team 6', 'Toto team 6 1', 'Toto team 6 2', 'Toto team 6 3'),
    ('Team 7', 'Full name team 7', 'Toto team 7 1', 'Toto team 7 2', 'Toto team 7 3'),
    ('Team 8', 'Full name team 8', 'Toto team 8 1', 'Toto team 8 2', 'Toto team 8 3'),
    ('Team 9', 'Full name team 9', 'Toto team 9 1', 'Toto team 9 2', 'Toto team 9 3'),
    ('Team 10', 'Full name team 10', 'Toto team 10 1', 'Toto team 10 2', 'Toto team 10 3'),
    ('Team 11', 'Full name team 11', 'Toto team 11 1', 'Toto team 11 2', 'Toto team 11 3'),
    ('Team 12', 'Full name team 12', 'Toto team 12 1', 'Toto team 12 2', 'Toto team 12 3'),
    ('Team 13', 'Full name team 13', 'Toto team 13 1', 'Toto team 13 2', 'Toto team 13 3'),
    ('Team 14', 'Full name team 14', 'Toto team 14 1', 'Toto team 14 2', 'Toto team 14 3'),
    ('Team 15', 'Full name team 15', 'Toto team 15 1', 'Toto team 15 2', 'Toto team 15 3'),
    ('Team 16', 'Full name team 16', 'Toto team 16 1', 'Toto team 16 2', 'Toto team 16 3')
]

R2 = [None, None, None, None, None, None, None, None]
R3 = [None, None, None, None]
LB = [None, None]
FINAL = [None, None]
THIRD = None
WINNER = None


R1order = [(0, 15), (7, 8), (3, 12), (4, 11), (1, 14), (6, 9), (2, 13), (5, 10)]

matchCount = 0

resultsLeft = [0, 0, 0]
resultsRight = [0, 0, 0]
totalLeft = 0
totalRight = 0
compsLeft = teams[0]
compsRight = teams[15]


class toto:
    def __init__(self, text):
        self.text = text


def getText(result):
    if result == -1:
        return 'DNF'
    else:
        return f'{(result/100):.2f}'


def updateTexts():
    global resultsLeft
    global resultsRight
    global totalLeft
    global totalRight
    global compsLeft
    global compsRight
    for i in range(3):
        with open(f'outputs/resultsleft{i+1}.txt', 'w') as outFile:
            outFile.write(getText(resultsLeft[i]))
        with open(f'outputs/resultsright{i+1}.txt', 'w') as outFile:
            outFile.write(getText(resultsRight[i]))
        with open(f'outputs/compsleft{i+1}.txt', 'w') as outFile:
            outFile.write(compsLeft[i + 2])
        with open(f'outputs/compsright{i+1}.txt', 'w') as outFile:
            outFile.write(compsRight[i + 2])
    with open('outputs/totalleft.txt', 'w') as outFile:
        outFile.write(getText(totalLeft))
    with open('outputs/totalright.txt', 'w') as outFile:
        outFile.write(getText(totalRight))
    with open('outputs/teamleft.txt', 'w') as outFile:
        outFile.write(compsLeft[1])
    with open('outputs/teamright.txt', 'w') as outFile:
        outFile.write(compsRight[1])
    if leftWins(totalLeft, totalRight):
        shutil.copyfile('RegionCup/winLeft.png', 'outputs/matchleft.png')
        shutil.copyfile('RegionCup/loseRight.png', 'outputs/matchright.png')
    elif leftWins(totalRight, totalLeft):
        shutil.copyfile('RegionCup/loseLeft.png', 'outputs/matchleft.png')
        shutil.copyfile('RegionCup/winRight.png', 'outputs/matchright.png')
    else:
        shutil.copyfile('RegionCup/emptyLeft.png', 'outputs/matchleft.png')
        shutil.copyfile('RegionCup/emptyRight.png', 'outputs/matchright.png')


def writeWinner(matchCount, winnerloser):
    global R2
    global R3
    global LB
    global THIRD
    global FINAL
    if matchCount < 8:
        with open(f'outputs/R2_{matchCount}.txt', 'w') as outFile:
            outFile.write(R2[matchCount][0])
        shutil.copyfile(f'RegionCup/{winnerloser[0]}.png', f'outputs/R1_{matchCount}_up.png')
        shutil.copyfile(f'RegionCup/{winnerloser[1]}.png', f'outputs/R1_{matchCount}_down.png')
    elif matchCount < 12:
        with open(f'outputs/R3_{matchCount - 8}.txt', 'w') as outFile:
            outFile.write(R3[matchCount - 8][0])
        shutil.copyfile(f'RegionCup/{winnerloser[0]}.png', f'outputs/R2_{matchCount - 8}_up.png')
        shutil.copyfile(f'RegionCup/{winnerloser[1]}.png', f'outputs/R2_{matchCount - 8}_down.png')
    elif matchCount < 14:
        with open(f'outputs/LB_{matchCount - 12}.txt', 'w') as outFile:
            outFile.write(LB[matchCount - 12][0])
        with open(f'outputs/FINAL_{matchCount - 12}.txt', 'w') as outFile:
            outFile.write(FINAL[matchCount - 12][0])
        shutil.copyfile(f'RegionCup/{winnerloser[0]}.png', f'outputs/R3_{matchCount - 12}_up.png')
        shutil.copyfile(f'RegionCup/{winnerloser[1]}.png', f'outputs/R3_{matchCount - 12}_down.png')
    elif matchCount == 14:
        with open(f'outputs/third.txt', 'w') as outFile:
            outFile.write(THIRD[0])
        shutil.copyfile(f'RegionCup/{winnerloser[0]}.png', f'outputs/LB_up.png')
        shutil.copyfile(f'RegionCup/{winnerloser[1]}.png', f'outputs/LB_down.png')
    elif matchCount == 15:
        with open(f'outputs/winner.txt', 'w') as outFile:
            outFile.write(WINNER[0])
        shutil.copyfile(f'RegionCup/{winnerloser[0]}.png', f'outputs/Final_up.png')
        shutil.copyfile(f'RegionCup/{winnerloser[1]}.png', f'outputs/Final_down.png')


def leftWins(totalLeft, totalRight):
    if totalLeft == -1:
        return False
    if totalRight == -1:
        return True
    if totalLeft < totalRight:
        return True
    return False


@bot.message_handler(commands=['next'])
def next(message):
    global matchCount
    global resultsLeft
    global resultsRight
    global totalLeft
    global totalRight
    global compsLeft
    global compsRight
    global R2
    global R3
    global LB
    global FINAL
    global THIRD
    global WINNER
    if matchCount < 8:
        if leftWins(totalLeft, totalRight):
            R2[matchCount] = compsLeft
        else:
            R2[matchCount] = compsRight
        if matchCount == 7:
            compsLeft = R2[0]
            compsRight = R2[1]
        else:
            compsLeft = teams[R1order[matchCount + 1][0]]
            compsRight = teams[R1order[matchCount + 1][1]]
    elif matchCount < 12:
        if leftWins(totalLeft, totalRight):
            R3[matchCount - 8] = compsLeft
        else:
            R3[matchCount - 8] = compsRight
        if matchCount == 11:
            compsLeft = R3[0]
            compsRight = R3[1]
        else:
            compsLeft = R2[2 * (matchCount - 8 + 1)]
            compsRight = R2[2 * (matchCount - 8 + 1) + 1]
    elif matchCount == 12:
        if leftWins(totalLeft, totalRight):
            FINAL[0] = compsLeft
            LB[0] = compsRight
        else:
            FINAL[0] = compsRight
            LB[0] = compsLeft
        compsLeft = R3[2]
        compsRight = R3[3]
    elif matchCount == 13:
        if leftWins(totalLeft, totalRight):
            FINAL[1] = compsLeft
            LB[1] = compsRight
        else:
            FINAL[1] = compsRight
            LB[1] = compsLeft
        compsLeft = LB[0]
        compsRight = LB[1]
    elif matchCount == 14:
        if leftWins(totalLeft, totalRight):
            THIRD = compsLeft
        else:
            THIRD = compsRight
        compsLeft = FINAL[0]
        compsRight = FINAL[1]
    elif matchCount == 15:
        if leftWins(totalLeft, totalRight):
            WINNER = compsLeft
        else:
            WINNER = compsRight
        compsLeft = FINAL[0]
        compsRight = FINAL[1]
    if leftWins(totalLeft, totalRight):
        winnerloser = ['winner', 'loser']
    else:
        winnerloser = ['loser', 'winner']
    resultsLeft = [0, 0, 0]
    resultsRight = [0, 0, 0]
    totalLeft = 0
    totalRight = 0
    updateTexts()
    writeWinner(matchCount, winnerloser)
    matchCount = matchCount + 1
    bot.send_message(groupId, f'Prochain match: {compsLeft[1]} vs {compsRight[1]}')
    bot.send_message(groupId, f'Left: {" ".join(compsLeft[2:])}')
    bot.send_message(groupId, f'Right: {" ".join(compsRight[2:])}')


@bot.message_handler(commands=['g'])
def left(message):
    global totalLeft
    result = int(message.text.removeprefix('/g '))
    for i in range(3):
        if resultsLeft[i] == 0:
            resultsLeft[i] = result
            break
    if -1 in resultsLeft:
        totalLeft = -1
    else:
        totalLeft = sum(resultsLeft)
    updateTexts()


@bot.message_handler(commands=['d'])
def right(message):
    global totalRight
    result = int(message.text.removeprefix('/d '))
    for i in range(3):
        if resultsRight[i] == 0:
            resultsRight[i] = result
            break
    if -1 in resultsRight:
        totalRight = -1
    else:
        totalRight = sum(resultsRight)
    updateTexts()


threadBot = threading.Thread(target=bot.polling)
threadBot.daemon = True
threadBot.start()

bot.send_message(groupId, 'Bot Regioncup prêt')
bot.send_message(groupId, f'Prochain match: {compsLeft[1]} vs {compsRight[1]}')
bot.send_message(groupId, f'Left: {" ".join(compsLeft[2:])}')
bot.send_message(groupId, f'Right: {" ".join(compsRight[2:])}')


for i in range(8):
    with open(f'outputs/R2_{i}.txt', 'w') as outFile:
        outFile.write('')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R1_{i}_up.png')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R1_{i}_down.png')
for i in range(8, 12):
    with open(f'outputs/R3_{i - 8}.txt', 'w') as outFile:
        outFile.write('')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R2_{i - 8}_up.png')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R2_{i - 8}_down.png')
for i in range(12, 14):
    with open(f'outputs/LB_{i - 12}.txt', 'w') as outFile:
        outFile.write('')
    with open(f'outputs/FINAL_{i - 12}.txt', 'w') as outFile:
        outFile.write('')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R3_{i - 12}_up.png')
    shutil.copyfile(f'RegionCup/empty.png', f'outputs/R3_{i - 12}_down.png')
with open(f'outputs/third.txt', 'w') as outFile:
    outFile.write('')
shutil.copyfile(f'RegionCup/empty.png', f'outputs/LB_up.png')
shutil.copyfile(f'RegionCup/empty.png', f'outputs/LB_down.png')
with open(f'outputs/winner.txt', 'w') as outFile:
    outFile.write('')
shutil.copyfile(f'RegionCup/empty.png', f'outputs/Final_up.png')
shutil.copyfile(f'RegionCup/empty.png', f'outputs/Final_down.png')


updateTexts()


while (True):
    pass
