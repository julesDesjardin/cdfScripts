import urllib.request
import json

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

activities = dict([])

events = {
    '333': '3x3',
    '222': '2x2',
    '444': '4x4',
    '555': '5x5',
    '666': '6x6',
    '777': '7x7',
    '333bf': 'Blind',
    '333fm': 'FMC',
    '333oh': 'OH',
    'clock': 'Clock',
    'minx': 'Mega',
    'pyram': 'Pyra',
    'skewb': 'Skewb',
    'sq1': 'Sq-1',
    '444bf': '4BLD',
    '555bf': '5BLD',
    '333mbf': 'Multiblind'
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
            event = events[codeSplit[0]]
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
            commands.append(f'genAssignment("{person["name"]}", "{activity}", "{roomActivity[id]}", "{colorActivity[id]}", "{task}")')

with open('outputs/plannings.txt', 'w', encoding='utf-8') as outFile:
    outFile.write("\n".join(commands))
