import urllib.request
import json

events = {
    '333': 4,
    '222': 3,
    '444': 3,
    '555': 2,
    '333bf': 2,
    '333oh': 3,
    'clock': 2,
    'minx': 2,
    'pyram': 3,
    'skewb': 3,
    'sq1': 2
}


def getReadableResult(result):
    output = ''
    if (result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output


print('Quel event ? Formats acceptés:')
print(events.keys())
chosenEvent = input()
while chosenEvent not in events:
    print('Mauvais format, recommencez')
    chosenEvent = input()

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

persons = dict([])

for person in data['persons']:
    persons[f"{person['registrantId']}"] = (person['name'], person['countryIso2'])

compFr = []
compEtranger = []

for event in data['events']:
    if event['id'] != chosenEvent:
        continue
    for result in event['rounds'][events[chosenEvent] - 2]['results']:
        (name, country) = persons[f"{result['personId']}"]
        if chosenEvent == '333bf':
            entry = (name, getReadableResult(result['best']))
        else:
            entry = (name, getReadableResult(result['average']))
        if country == 'FR':
            compFr.append(entry)
        else:
            compEtranger.append(entry)
        if len(compFr) == 12:
            break

with open('outputs/Recap.txt', 'w', encoding='utf-8') as outFile:
    outFile.write(f'{chosenEvent}\n\n\n')
    outFile.write(f'{len(compFr) + len(compEtranger)} compétiteurs au total\n\n')
    if len(compEtranger) > 12:
        outFile.write(
            f'ATTENTION PLUS DE 12 ETRANGERS.{", ".join([comp[1] for comp in compEtranger[12:]])} ne seront pas comptabilisés, à rajouter après.\n')
        compEtranger = compEtranger[:12]
    else:
        while len(compEtranger) < 12:
            compEtranger.append(('', ''))
    vert = [
        compFr[7],
        compFr[5],
        compFr[3],
        compFr[1],
        compEtranger[3],
        compEtranger[1],
        compFr[11],
        compFr[9],
        compEtranger[11],
        compEtranger[9],
        compEtranger[7],
        compEtranger[5]
    ]
    violet = [
        compFr[0],
        compFr[2],
        compFr[4],
        compFr[6],
        compFr[8],
        compFr[10],
        compEtranger[0],
        compEtranger[2],
        compEtranger[4],
        compEtranger[6],
        compEtranger[8],
        compEtranger[10]
    ]
    outFile.write('Zone verte / Green zone:\n')
    for i in range(12):
        outFile.write(f'{i+1}. {vert[i][0]}\n')
    outFile.write('\n')
    outFile.write('Zone violette / Purple zone:\n')
    for i in range(12):
        outFile.write(f'{i+1}. {violet[i][0]}\n')

    outFile.write('\nPrésentation :\n')
    outFile.write('Etrangers :\n')
    for i in range(11, -1, -1):
        if compEtranger[i][0] != '':
            outFile.write(f'{compEtranger[i][0]} ({compEtranger[i][1]})\n')
    outFile.write('Francais :\n')
    for i in range(11, -1, -1):
        outFile.write(f'{i+1}. {compFr[i][0]} ({compFr[i][1]})\n')
