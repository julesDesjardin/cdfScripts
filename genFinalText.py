import threading
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from Common import TelegramBot
import time


DNF_ATTEMPT = 30 * 60 * 100  # 30 min, so an avg5/mo3 goes higher than 10 min
DNF_RESULT = 10 * 60 * 100  # 10 min

recordSingles = {
    '333': '4.44 (Juliette Sébastien)',
    '222': '0.78 (Juliette Sébastien)',
    '444': '21.48 (Alexandre Carlier)',
    '555': '41.23 (Abdelhak Kaddour)',
    '666': '1:20.21 (Peter Grassard)',
    '777': '2:04.41 (Abdelhak Kaddour)',
    '333bf': '13.22 (Charles Daloz-Baltenberger)',
    '333fm': '18 (Louis Sarthou & Louis-Marie Ratto)',
    '333oh': '6.92 (Juliette Sébastien)',
    'clock': '2.19 (César Essling)',
    'minx': '27.78 (Ulysse Merlin)',
    'pyram': '1.15 (Diego Alfonso)',
    'skewb': '1.18 (Maxence Baudry)',
    'sq1': '5.17 (Thibaud Ou)',
    '444bf': '1:46.47 (Tiago Eche)',
    '555bf': '5:17.35 (Willian Phommaha)',
    '333mbf': '37/39 57:00 (Maxime Madrzyk)'
}
recordAverages = {
    '333': '5.81 (Juliette Sébastien)',
    '222': '1.39 (John Bacouël)',
    '444': '25.87 (Alexandre Carlier)',
    '555': '46.21 (Abdelhak Kaddour)',
    '666': '1:24.55 (Abdelhak Kaddour)',
    '777': '2:11.69 (Abdelhak Kaddour)',
    '333bf': '17.02 (Charles Daloz-Baltenberger)',
    '333fm': '20.67 (Louis-Marie Ratto)',
    '333oh': '9.07 (Juliette Sébastien)',
    'clock': '2.97 (Baptiste Bery)',
    'minx': '31.77 (Rémi Perrin)',
    'pyram': '1.88 (Diego Alfonso)',
    'skewb': '1.89 (Anthony Lafourcade)',
    'sq1': '6.52 (Nikita Frétay--Bayart)',
    '444bf': '2:28.93 (Arthur Garcin)',
    '555bf': '7:29.51 (Willian Phommaha)',
    '333mbf': 'null'
}


CRITERIA = dict([
    ('333', 'average'),
    ('222', 'average'),
    ('444', 'average'),
    ('555', 'average'),
    ('666', 'mean'),
    ('777', 'mean'),
    ('333bf', 'average'),
    ('333fm', 'mean'),
    ('333oh', 'average'),
    ('clock', 'average'),
    ('minx', 'average'),
    ('pyram', 'average'),
    ('skewb', 'average'),
    ('sq1', 'average'),
    ('444bf', 'mean'),
    ('555bf', 'mean'),
    ('333mbf', 'mean'),
])


def getQueryResult(query):
    url = 'https://live.worldcubeassociation.org/api'
    transport = AIOHTTPTransport(url=url)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(gql(query))


def getReadableResult(result):
    if (result >= DNF_RESULT):
        return 'DNF'
    output = ''
    if (result >= 6000):
        output = output + f'{int(result / 6000)}:'
    result = result % 6000
    output = output + f'{int(result / 100):02}.{result % 100:02}'
    return output


def finalTextCallback(message):

    print('Received')
    messageSplit = message.split()
    event = messageSplit[0]
    number = int(messageSplit[1])

# 10228
    query = f'''
    query MyQuery {{
        competition(id: "10122") {{
            competitionEvents {{
                event {{
                    id
                }}
                rounds {{
                    id
                    number
                }}
            }}
        }}
    }}
    '''

    ids = []
    found = False
    result = getQueryResult(query)
    print('Comp found')
    for competitionEvent in result['competition']['competitionEvents']:
        if found:
            break
        if (competitionEvent['event']['id'] == event):
            for round in competitionEvent['rounds']:
                if (round['number'] < number):
                    ids.append(int(round['id']))
                    criteria = CRITERIA[event]
                    found = True

    if not found:
        return

    bestSingle = DNF_RESULT
    bestAverage = DNF_RESULT
    personSingle = ''
    personAverage = ''
    for id in ids:
        query = f'''
        query MyQuery {{
        round(id: "{id}") {{
            results {{
                person {{
                    name
                    id
                    registrantId
                    country {{
                    iso2
                    }}
                }}        
                attempts {{
                    result
                }}
            }}
        }}
        }}
        '''

        queryResult = getQueryResult(query)
        print('Results found')
        for result in queryResult['round']['results']:
            if result['person']['country']['iso2'] != 'FR':
                continue
            results = []
            for attempt in result['attempts']:
                if attempt['result'] == 0:
                    continue
                if attempt['result'] < 0:
                    nonDNFResult = DNF_ATTEMPT
                else:
                    nonDNFResult = attempt['result']
                if (nonDNFResult < bestSingle):
                    bestSingle = nonDNFResult
                    personSingle = result['person']['name']
                results.append(nonDNFResult)
            if criteria == 'mean':
                if len(results) < 3:
                    break
                average = sum(results) // 3
            else:
                if len(results) < 5:
                    break
                average = (sum(results) - min(results) - max(results)) // 3
            if average < bestAverage:
                bestAverage = average
                personAverage = result['person']['name']

    print('Best founds')
    with open('NRSingle.txt', 'w', encoding='utf-8') as textSingle:
        textSingle.write(f'Single: {recordSingles[event]}')
    with open('NRAverage.txt', 'w', encoding='utf-8') as textAverage:
        textAverage.write(f'{criteria}: {recordAverages[event]}')
    with open('BestSingle.txt', 'w', encoding='utf-8') as textSingle:
        textSingle.write(f'Single: {getReadableResult(bestSingle)} ({personSingle})')
    with open('BestAverage.txt', 'w', encoding='utf-8') as textAverage:
        textAverage.write(f'{criteria}: {getReadableResult(bestAverage)} ({personAverage})')
    print('done')


bot = TelegramBot.TelegramBot('', '', True, True)
bot.sendSimpleMessage('Bot Texts ready')
bot.setMessageHandler(['timeTowerEvent'], finalTextCallback)
threadBot = threading.Thread(target=bot.startPolling)
threadBot.daemon = True
threadBot.start()
while (True):
    pass
