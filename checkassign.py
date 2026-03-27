import urllib.request
import json

with urllib.request.urlopen("https://www.worldcubeassociation.org/api/v0/competitions/FrenchChampionship2026/wcif/public") as url:
    data = json.loads(url.read().decode())

activitiesR1 = dict([])
activitiesR2 = dict([])

for room in data['schedule']['venues'][0]['rooms']:
    for activity in room['activities']:
        for child in activity['childActivities']:
            id = child['id']
            code = child['activityCode']
            codeSplit = code.split('-')
            if codeSplit[1] == 'r1':
                activitiesR1[f'{id}'] = codeSplit[0]
            if codeSplit[1] == 'r2':
                activitiesR2[f'{id}'] = codeSplit[0]

for person in data['persons']:
    assignsR1 = dict([])

    for assignment in person['assignments']:
        if assignment['assignmentCode'] != 'competitor':
            continue
        id = assignment['activityId']
        if f'{id}' in activitiesR1:
            event = activitiesR1[f'{id}']
            if event in assignsR1:
                print(f"Duplicate Competitor assignment for {person['name']} in {event}")
            assignsR1[event] = 'toto'

    if person['registration'] is None:
        continue
    for event in person['registration']['eventIds']:
        if event not in assignsR1:
            print(f"Missing assignment for {person['name']} in {event}")
    for event in assignsR1:
        if event not in person['registration']['eventIds']:
            print(f"{person['name']} wrongly assigned in {event}")
