import telebot
import threading
import keys
import time
import shutil

groupId = keys.ID
bot = telebot.TeleBot(keys.TOKEN)

teams = [
    # ('AuRA 1', 'Auvergne-Rhône-Alpes 1', 'Juliette Sébastien', 'Mathis Luc', 'Simon Eyraud'),
    # ('Nouvelle-Aq. 1', 'Nouvelle-Aquitaine 1', 'Alexandre Carlier', 'Quentin Rivault', 'Elian Beguec'),
    # ('IDF 1', 'Île-de-France 1', 'Lucas Déglise', 'Yassine Dammak', 'Joris Arias Capes'),
    # ('Grand Est 1', 'Grand Est 1', 'Valentin Hoffmann', 'Victor Colin', 'Charles Daloz-Baltenberger'),
    ('HdF', 'Hauts-de-France', 'Fanny Pousset', 'Victor Wijsman', 'Louis Fertier'),
    ('PACA', 'Provence-Alpes-Côte d\'Azur', 'Nicolas Gertner Kilian', 'Adrien Neveu', 'Marie Vincent'),
    ('CVdL', 'Centre-Val de Loire', 'Arthur Garcin', 'Samuel Jehanno', 'Victor Chenu'),
    # ('BFC 1', 'Bourgogne-Franche-Comté 1', 'Peter Grassard', 'Nils Rödel', 'Gaspard Carré'),
    ('Bretagne', 'Bretagne', 'Anton Piau', 'Hippolyte Moreau', 'Louis Sarthou'),
    ('Occitanie', 'Occitanie', 'Manu Dutheil', 'Dorian Thomas', 'Wilfrid Py'),
    ('Outre-Mer', 'Outre-Mer', 'Étienne Aubry', 'Kévin Ky', 'Mathis Schecroun'),
    ('Normandie', 'Normandie', 'Adrien Vallée', 'César Essling', 'Maël Tran'),
    ('PdlL', 'Pays de la Loire', 'Zoé Ruth', 'Louis Presti', 'Kilian Farrell'),
    ('Corse', 'Corse', 'Jonathan Dammann', 'Manon Bernard', 'Antoine Martini'),
    # ('IDF 2', 'Île-de-France 2', 'Abdelhak Kaddour', 'Pablo Contreras', 'Louis-Marie Ratto'),
    # ('Nouvelle-Aq. 2', 'Nouvelle-Aquitaine 2', 'Jean-Charles Tillit', 'Alexis Le Merrer', 'Malo Coraboeuf'),
]
# ('AuRA 2', 'Auvergne-Rhône-Alpes 2', 'Baptiste Bery', 'Sylvain Favier', 'Armand Lemarinier'),
# ('Grand Est 2', 'Grand Est 2', 'Maxence Baudry', 'Paul Luciw', 'Yannick Beyer'),
# ('BFC 2', 'Bourgogne-Franche-Comté 2', 'Ylann Vernaton', 'Baptiste Dano', 'Thomas Pianeta'),
# ('AuRA 3', 'Auvergne-Rhône-Alpes 3', 'Ilona Ansel', 'Noé Bourdon', 'Samuel Dechaume-Moncharmont'),
# ('IDF 3', 'Île-de-France 3', 'Jaimy Mfoumou', 'Hélie de Palmaert', 'Lev Azaria Doron'),
# ('Nouvelle-Aq. 3', 'Nouvelle-Aquitaine 3', 'Titouan Rincon', 'Hugo Guillet', 'Florian Bernard'),
# ('Grand Est 3', 'Grand Est 3', 'Mathis Audibert', 'Nathan Vogel-Brustolin', 'Valentin Moutte'),
# ('BFC 3', 'Bourgogne-Franche-Comté 3', 'Erwan Pacquentin', 'Melwin Pacquentin', 'Maël Pacquentin'),
# ('AuRA 4', 'Auvergne-Rhône-Alpes 4', 'Anael Champion', 'Diego Alfonso', 'Virgile Perrot'),
# ('AuRA 5', 'Auvergne-Rhône-Alpes 5', 'Marianne Faure', 'Marc de Joussineau', 'Maxime Madrzyk'),

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
    if result == 0:
        for i in range(2, -1, -1):
            if resultsLeft[i] != 0:
                resultsLeft[i] = 0
                break
    else:
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
    if result == 0:
        for i in range(2, -1, -1):
            if resultsRight[i] != 0:
                resultsRight[i] = 0
                break
    else:
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


def testrun(side):
    time.sleep(10)
    if (side):
        right(toto('/d 100'))
    else:
        left(toto('/g 100'))
    next(toto(''))


while (True):
    pass
