import urllib.request
import json

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

activities = dict([])

events = {
    '333': ('3x3', 4),
    '222': ('2x2', 3),
    '444': ('4x4', 3),
    '555': ('5x5', 2),
    '666': ('6x6', 1),
    '777': ('7x7', 1),
    '333bf': ('Blind', 2),
    '333fm': ('FMC', 1),
    '333oh': ('OH', 3),
    'clock': ('Clock', 2),
    'minx': ('Mega', 2),
    'pyram': ('Pyra', 3),
    'skewb': ('Skewb', 3),
    'sq1': ('Sq-1', 2),
    '444bf': ('4BLD', 1),
    '555bf': ('5BLD', 1),
    '333mbf': ('Multiblind', 1)
}

tasks = {
    'competitor': 'Comp',
    'staff-stagelead': 'Orga',
    'staff-other': 'Unoff',
    'staff-dataentry': 'Score',
    'staff-delegate': 'Deleg',
    'staff-judge': 'Judge',
    'staff-scrambler': 'Scr',
    'staff-runner': 'Run',
    'staff-announcer': 'Acc',
}

colors = {
    'Main Green': '#4CD74A',
    'Main Purple': '#7F6AFF',
    'Side Orange': '#FF7338',
    'Side White': "#FFEBCB",
}

colorActivity = dict([])
roomActivity = dict([])
for room in data['schedule']['venues'][0]['rooms']:
    for activity in room['activities']:
        for child in activity['childActivities']:
            id = child['id']
            code = child['activityCode']
            codeSplit = code.split('-')
            (event, eventRound) = events[codeSplit[0]]
            if (event == '6x6' or event == '7x7'):
                activities[f'{id}'] = [f'{event} F - {codeSplit[2].upper()}']
            elif event == '4BLD':
                activities[f'{id}'] = [f'{event} - {codeSplit[2].upper()}']
            elif event == '5BLD':
                activities[f'{id}'] = [f'{event}']
            elif event == 'Multiblind':
                activities[f'{id}'] = [f'{event}', 'Submit MBLD']
            elif event == 'FMC':
                activities[f'{id}'] = [f'{event} - A1', f'{event} - A2', f'{event} - A3']
            else:
                roundNumber = int(codeSplit[1][1])
                if roundNumber == eventRound:
                    activities[f'{id}'] = [f'{event} F']
                else:
                    activities[f'{id}'] = [f'{event} {codeSplit[1].upper()} - {codeSplit[2].upper()}']
            colorActivity[f'{id}'] = colors[room['name']]
            roomActivity[f'{id}'] = room['name'].split(' ')[0].lower()

commands = []
commands.append('removeSheets()')
for person in sorted(data['persons'], key=lambda x: x['name']):
    if person['registration'] is None:
        continue

    commands.append(f'createCompetitor("{person["name"]}")')

    for assignment in person['assignments']:
        id = f"{assignment['activityId']}"
        task = tasks[assignment['assignmentCode']]
        for activity in activities[id]:
            if activity == 'Submit MBLD' and task == 'Judge':
                pass
            else:
                commands.append(f'genAssignment("{person["name"]}", "{activity}", "{roomActivity[id]}", "{colorActivity[id]}", "{task}")')

commands.append('createCompetitor("Laurent Reynaud")')
commands.append('createCompetitor("Tifenn Le Roy")')
commands.append(f'genAssignment("Tifenn Le Roy", "Skewb R1 - G3", "main", "{colors["Main Green"]}", "Acc")')
commands.append(f'genAssignment("Tifenn Le Roy", "Skewb R1 - G4", "main", "{colors["Main Green"]}", "Acc")')
commands.append(f'genAssignment("Tifenn Le Roy", "Pyra R2 - G2", "main", "{colors["Main Green"]}", "Acc")')
commands.append(f'genAssignment("Tifenn Le Roy", "OH R2 - G1", "main", "{colors["Main Green"]}", "Acc")')
commands.append(f'genAssignment("Tifenn Le Roy", "OH R2 - G2", "main", "{colors["Main Green"]}", "Acc")')
commands.append(f'genAssignment("Tifenn Le Roy", "3x3 R1 - G4", "main", "{colors["Main Green"]}", "Acc")')
with open('outputs/plannings.txt', 'w', encoding='utf-8') as outFile:
    outFile.write("\n".join(commands))
