import telebot
import threading
import keys
import urllib.request
import json
from playsound3 import playsound
import shutil

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

groupId = keys.ID
bot = telebot.TeleBot(keys.TOKEN)

events = {
    '333': ('3x3', 4),
    '222': ('2x2', 3),
    '444': ('4x4', 3),
    '555': ('5x5', 2),
    '666': ('6x6', 1),
    '777': ('7x7', 1),
    '333bf': ('3BLD', 2),
    '333fm': ('FMC', 1),
    '333oh': ('OH', 3),
    'clock': ('Clock', 2),
    'minx': ('Megaminx', 2),
    'pyram': ('Pyraminx', 3),
    'skewb': ('Skewb', 3),
    'sq1': ('Square-1', 2),
    '444bf': ('4BLD', 1),
    '555bf': ('5BLD', 1),
    '333mbf': ('Multi', 1)
}

groupsMain = []
groupsSide = []

for activity in data['schedule']['venues'][0]['rooms'][0]['activities']:
    toEnter = []
    if len(activity['childActivities']) == 0:
        toEnter.append(activity)
    else:
        for child in activity['childActivities']:
            toEnter.append(child)
    for child in toEnter:
        groupsMain.append((child['activityCode'], child['startTime']))
groupsMain.sort(key=lambda x: x[1])
groupsMain.append(('other-end',-1))
groupsMain.append(('other-end',-1))

for activity in data['schedule']['venues'][0]['rooms'][2]['activities']:
    toEnter = []
    if len(activity['childActivities']) == 0:
        toEnter.append(activity)
    else:
        for child in activity['childActivities']:
            toEnter.append(child)
    for child in toEnter:
        groupsSide.append((child['activityCode'], child['startTime']))

groupsSide.sort(key=lambda x: x[1])
groupsSide.append(('other-end',-1))
groupsSide.append(('other-end',-1))

mainIndex = 0
sideIndex = 0


def getTime(room, index):
    if room == 'main':
        if groupsMain[index][1]:
            return ''
        timestamp = groupsMain[index][1][11:19]
    else:
        if groupsSide[index][1]:
            return ''
        timestamp = groupsSide[index][1][11:19]
    heure = int(timestamp[0:2])
    return f'{heure + 2}{timestamp[2:]}'


def getText(room, index):
    if room == 'main':
        event = groupsMain[index][0]
    else:
        event = groupsSide[index][0]
    eventSplit = event.split('-')
    if eventSplit[0] == 'other':
        match eventSplit[1]:
            case 'checkin':
                text = 'Check-in'
            case 'lunch':
                text = 'Lunch'
            case 'misc':
                text = 'Coupe de France'
            case 'multi':
                text = 'Dropoff multi'
            case 'end':
                text = ''
    else:
        (eventName, eventRound) = events[eventSplit[0]]
        text = eventName
        match eventName:
            case 'Multiblind':
                pass
            case 'FMC':
                text += f'\nAttempt {eventSplit[2][1]}'
            case '6x6' | '7x7':
                text += f'\nFinal Group {eventSplit[2][1]}'
            case default:
                roundNumber = int(eventSplit[1][1])
                if roundNumber == eventRound:
                    text += f'\nFinal'
                elif roundNumber == eventRound - 1 and eventRound == 3:
                    text += f'\nSemi-Final Group {eventSplit[2][1]}'
                elif roundNumber == eventRound - 1 and eventRound == 4:
                    text += f'\nSemi-Final'
                else:
                    text += f'\nRound {roundNumber} Group {eventSplit[2][1]}'
    return text


def updateEvent(room):
    global mainIndex
    global sideIndex
    if room == 'main':
        fileNow = 'mainNow.txt'
        fileNext = 'mainNext.txt'
        imgNow = 'mainNow.png'
        imgNext = 'mainNext.png'
        index = mainIndex
        event = groupsMain[index][0]
        nextEvent = groupsMain[index + 1][0]
    else:
        fileNow = 'sideNow.txt'
        fileNext = 'sideNext.txt'
        imgNow = 'sideNow.png'
        imgNext = 'sideNext.png'
        index = sideIndex
        event = groupsSide[index][0]
        nextEvent = groupsSide[index + 1][0]
    with open(f'outputs/{fileNow}', 'w') as fileWrite:
        fileWrite.write(getText(room, index))
    with open(f'outputs/{fileNext}', 'w') as fileWrite:
        fileWrite.write(getText(room, index + 1))
    eventId = event.split('-')[0]
    shutil.copyfile(f'event/{eventId}.png', f'outputs/{imgNow}')
    eventId = nextEvent.split('-')[0]
    shutil.copyfile(f'event/{eventId}.png', f'outputs/{imgNext}')


def sendUpdate(room):
    if room == 'main':
        index = mainIndex
    else:
        index = sideIndex
    bot.send_message(groupId, f'{room} mise à jour : {getText(room, index)}, heure: {getTime(room, index)}')
    bot.send_message(groupId, f'Prochain : {getText(room, index + 1)}, heure: {getTime(room, index + 1)}')


@bot.message_handler(commands=['nextmain'])
def nextMainCallback(_):
    global mainIndex
    mainIndex = mainIndex + 1
    updateEvent('main')
    sendUpdate('main')


@bot.message_handler(commands=['nextside'])
def nextSideCallback(_):
    global sideIndex
    sideIndex = sideIndex + 1
    updateEvent('side')
    sendUpdate('side')


@bot.message_handler(commands=['prevmain'])
def prevMainCallback(_):
    global mainIndex
    mainIndex = mainIndex - 1
    updateEvent('main')
    sendUpdate('main')


@bot.message_handler(commands=['prevside'])
def prevSideCallback(_):
    global sideIndex
    sideIndex = sideIndex - 1
    updateEvent('side')
    sendUpdate('side')


@bot.message_handler(commands=['setmain'])
def setMainCallback(message):
    chosenIndex = int(message.text.removeprefix('/setmain '))
    global mainIndex
    mainIndex = chosenIndex
    updateEvent('main')
    sendUpdate('main')


@bot.message_handler(commands=['setside'])
def setMainCallback(message):
    chosenIndex = int(message.text.removeprefix('/setside '))
    global sideIndex
    sideIndex = chosenIndex
    updateEvent('side')
    sendUpdate('side')


@bot.message_handler(commands=['resetsamedi', 'resetdimanche', 'resetlundi'])
def resetCallback(message):
    global mainIndex
    global sideIndex
    chosenDate = message.text.removeprefix('/reset')
    mainIndex = 0
    sideIndex = 0
    match chosenDate.lower().strip():
        case 'lundi':
            startDate = '2026-04-06'
        case 'dimanche':
            startDate = '2026-04-05'
        case default:
            startDate = '2026-04-04'
    while not groupsMain[mainIndex][1].startswith(startDate):
        mainIndex = mainIndex + 1
    while not groupsSide[sideIndex][1].startswith(startDate):
        sideIndex = sideIndex + 1
    updateEvent('main')
    updateEvent('side')
    bot.send_message(groupId, f'Reset fait pour {chosenDate}')
    sendUpdate('main')
    sendUpdate('side')


@bot.message_handler(commands=['ding'])
def dingCallback(_):
    playsound('announcement.mp3')
    bot.send_message(groupId, 'Ding fait')


threadBot = threading.Thread(target=bot.polling)
threadBot.daemon = True
threadBot.start()

bot.send_message(groupId, 'Bot groups prêt')

while (True):
    pass
