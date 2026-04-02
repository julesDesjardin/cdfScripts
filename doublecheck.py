import urllib.request
import json

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

activities = dict([])
groups = dict([])
doublecheck = dict([])
rooms = dict([])

for room in data['schedule']['venues'][0]['rooms']:
    for activity in room['activities']:
        for child in activity['childActivities']:
            id = child['id']
            code = child['activityCode']
            codeSplit = code.split('-')
            activities[f'{id}'] = codeSplit[0]
            groups[f'{id}'] = codeSplit[2]
            rooms[f'{id}'] = room['name'].split(' ')[1]

for person in data['persons']:
    if person['wcaId'] is None:
        continue
    for assignment in person['assignments']:
        if assignment['assignmentCode'] != 'competitor':
            continue
        id = assignment['activityId']
        if activities[f'{id}'] in ['333fm', '444bf', '555bf', '333mbf']:
            continue
        for pb in person['personalBests']:
            if pb['eventId'] == activities[f'{id}']:
                if pb['nationalRanking'] > 15:
                    continue
                if f'{id}' not in doublecheck:
                    doublecheck[f'{id}'] = [person['name']]
                elif person['name'] not in doublecheck[f'{id}']:
                    doublecheck[f'{id}'].append(person['name'])

stuff = []
for id in doublecheck:
    for person in doublecheck[id]:
        stuff.append((activities[id], rooms[id], groups[id], person))

stuff.sort(key=lambda x: x[3])
stuff.sort(key=lambda x: x[2])
stuff.sort(key=lambda x: x[0])
stuff.sort(key=lambda x: x[1])

currEvent = ''
currRoom = ''
currGroup = ''

dataToPrint = []
for truc in stuff:
    (event, room, group, person) = truc
    if event != currEvent or room != currRoom or group != currGroup:
        currEvent = event
        currRoom = room
        currGroup = group
        dataToPrint.append('')
        dataToPrint.append(f'{event} {room} - Groupe {group[1]}')
    dataToPrint.append(person)

with open('toto.txt', 'w', encoding='utf-8') as dataOut:
    dataOut.write('\n'.join(dataToPrint))
