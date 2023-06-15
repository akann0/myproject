from urllib.request import Request, urlopen
import json

league_ids = [82]
PP_API = "https://api.prizepicks.com/projections"



def findpp():
    bets = []
    req = Request(
        url=PP_API, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    webpage = urlopen(req).read()

    stringy = str(webpage)

    for i in range(len(stringy)):
        if stringy[i:i+1] == "\\":
            stringy = stringy[:i] + stringy[i+1:]


    converted = json.loads(stringy[2:-2])

    data_dict = {}

    print(converted["data"][0])
    for item in converted['data'][1]:
        print(item)

    data = converted["data"]
    for item in data:
        pid = item["relationships"]["new_player"]["data"]["id"]
        ls = item["attributes"]["line_score"]
        stattype = item["attributes"]["stat_type"]
        if (pid in data_dict.keys()):
            data_dict[pid].append([ls, stattype])
        else:
            data_dict[pid] = [[ls, stattype]]


    players = converted["included"]
    playerlist_by_team = {}


    print(players[0])

    #fill players_dict with name:id
    for player in players:
        if ("new_player" == player["type"]):
            if (player["attributes"]['league_id'] in league_ids):
                for_pl = {
                    'name': player["attributes"]['name']
                }
                for prop in data_dict[player['id']]:
                    for_pl[prop[1]] = prop[0]
                if player['attributes']['team'] in playerlist_by_team.keys():
                    playerlist_by_team[player['attributes']['team']].append(for_pl)
                else:
                    playerlist_by_team[player['attributes']['team']] = [for_pl]
        else:
            
            #print(player)
            continue
    
    print(playerlist_by_team)
    return playerlist_by_team

#findpp()