import csv
from ppscrape import findpp
prizepicks = findpp()
playerdata = []
with open('playerdata.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        playerdata.append(row)

def getview():
    answer = ""
    for team in prizepicks:
        #print(team)
        if (team in ["Milan", "Torino"]):
            for player in prizepicks[team]:
                for player_data in playerdata:
                    if player["name"] == player_data["pname"]:
                        #print(player["name"])
                        #print(player_data["pname"])
                        for stat in player:
                            #print(stat)
                            if stat in player_data.keys():
                                print(player["name"] + " " + stat)
                                print(player[stat])
                                print(int(player_data[stat]) / float(player_data["nineties"]))
                                answer += player["name"] + " " + stat + " " + str(player[stat]) + " " + str(int(player_data[stat]) / float(player_data["nineties"]))
    

    return answer

getview()