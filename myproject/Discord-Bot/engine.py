import discord
import os
import random
import time
import csv
import misc

offlineup = []
deflineup = []
poss = 0
homelineup = []
awaylineup = []
minute = 0
setpieces = []
events = []

def side(player):
    if player == 2:
        return 7
    if player == 7:
        return 2
    if player == 11:
        return 5
    if player == 5:
        return 11  

def attackers(pos = False, z = True):
    global offlineup
    f = misc.form(offlineup[0])
    f.reverse()
    rme = list()
    for p in f:
        if p == 'M':
            break
        elif isinstance(p,str) and not pos:
            continue
        else:
            rme.append(p)
    if z:
        rme.append(0)
    return rme


def counterattackers():
    global offlineup
    ca = list()
    AM = False
    f = misc.form(offlineup[0])
    f.reverse()
    for attacker in f:
        if attacker == 'ST':
            AM = True
        elif attacker == 'AM':
            break
        elif AM:
            if random.random() < misc.ranB(0.8, int(pid2bute(deflineup[int(AM)], 'rating'))):
                ca.append(attacker)
        else:
            ca.append(attacker)
    return misc.tts(ca)

def counterdefenders():
    global deflineup
    ca = list()
    DM = False
    for defender in misc.form(deflineup[0]):
        if defender == 'DM':
            DM = True
        elif defender == 'M':
            break
        elif DM:
            if random.random() < misc.ranB(0.8, int(pid2bute(deflineup[int(DM)], 'rating'))):
                ca.append(defender)
        else:
            ca.append(defender)
    return misc.tts(ca)


def crossrecvrs(player):
    RMe = [10,9,7,11]
    if player == 2 or player == 7:
        RMe.remove(7)
        RMe.append(6)
    elif player == 5 or player == 11:
        RMe.remove(11)
        RMe.append(8)
    else:	
        RMe.append(random.choice([6,8]))
    if player in RMe:
        RMe.remove(player)
    return RMe


def roal(chance):
    global minute
    global offlineup
    if len(chance) > 2:
        if chance[-2][1] != chance[-3][1]:
            assist = ", assissted by " + pid2bute(offlineup[(chance[-3][1])], 'playername')
        else:
            assist = ", unassisted"
    else:
        assist = ", unassisted"
    sequence = misc.sequence(chance)
    return (pid2bute(offlineup[(chance[-1][1])], 'playername') + " " +str(minute) + assist + sequence)

def setpiece(offinthebox, definthebox, difficulty = 0.333):
    global poss
    global setpieces
    box = []
    if difficulty == 0.333:
        typ = 'corner'
    else:
        typ = 'setpiece'
    chance = [['deadball', setpieces[poss][0], 1]]
    for off in range(offinthebox):
        box.append('off ' + str(setpieces[poss][off+1]))
    for off in range(definthebox):
        box.append('def ' + str(setpieces[1-poss][off+1]))
    words = (random.choice(box)).split()
    if words[0] == 'off':
        chance.append([typ, int(words[1]), misc.ranB(difficulty, int(pid2bute(offlineup[setpieces[poss][0]], 'rating')), True)])
        chance.append(['shot', int(words[1]), misc.ranB(0.25, int(pid2bute(offlineup[int(words[1])], 'rating')), True)])
    else:
        chance.append(['clearance', str(10-definthebox)+ ' ' +str(10-offinthebox), misc.ranB(0.8, int(pid2bute(deflineup[int(words[1])], 'rating')), True)])
    return chance

	

def nex(chance, whodere=[]):
    global offlineup
    global deflineup
    passr = chance[-1][1]
    posib = attackers()
    if chance[-1][0] == 'keypass' or chance[-1][0] == 'dribble':
        posib = [0,0,0,0,0,0,0,0,7,9,10,11]
    if len(chance) == 1 and chance[0][0] == 'thru':
        posib = [2,7,11,5]
    if chance[0][0] == 'counter':
        posib = list()
        for attacker in whodere[0]:
            posib.append(attacker)
        if len(chance) > 3:
            for x in range(2 ** (len(chance)-3)):
                posib.append(99)
    if passr in posib:
        posib.remove(passr)
    if (((chance[-1][0] == 'short' or len(chance) == 1) and chance[0][0] == 'sequence') or (len(chance) < 2 and chance[0][0] == 'thrumid') or (chance[-1][0] != 'cutback' and chance[0][0] == 'thru' and chance[-1][0] != 'cross')) and (0 in posib):
        posib.remove(0)
    if len(chance) > 1 and chance[0][0] == 'thrumid':
        posib = [0]
    if len(chance) == 2 and chance[0][0] == 'thru':
        posib = [passr, side(passr),7,8,9,10,11,17,17]
    if chance[-1][0] == 'precross':
        posib = [17]
    if chance[-1][0] == 'predribble':
        posib = [passr]
    if chance[-1][0] == 'cross' or chance[-1][0] == 'cutback':
        posib = [99]
    #print(posib)
    recvr = random.choice(posib)
    #print(recvr)
    if recvr == 17:
        return ['cross', random.choice(crossrecvrs(passr)), misc.ranpow(1.5, int(pid2bute(offlineup[passr], 'rating')))]
    elif chance[0][0] == 'counter' and (recvr != 0 and recvr != 99):
        return ['short', recvr, misc.ranpow(2 ** (len(whodere[1]) - len(whodere[0])), int(pid2bute(offlineup[passr], 'rating')))]
    elif chance[0][0] == 'sequence' and (recvr != 0 and recvr != 99):
        if chance[-1][0] == 'short':
            if random.random() > (0.975) ** (len(chance)):
                return ['keypass', recvr,misc.ranpow(1.25, int(pid2bute(offlineup[passr], 'rating')))]
            else:
                return ['short', recvr,misc.ranpow(0.25, int(pid2bute(offlineup[passr], 'rating')))]
        elif chance[-1][0] == 'keypass' or chance[-1][0] == 'dribble':
            return ['cutback', recvr,misc.ranpow(1, int(pid2bute(offlineup[passr], 'rating')))]
        elif recvr == passr:
            return ['dribble', recvr,misc.ranpow(1.75, int(pid2bute(offlineup[passr], 'rating')))]
        else:
            return ['short', recvr,misc.ranpow(0.5, int(pid2bute(offlineup[passr], 'rating')), True)]
    elif (recvr != 0 and recvr != 99) and chance[0][0] == 'thrumid':
        return['thruongoal', recvr, misc.ranpow(8, int(pid2bute(offlineup[passr], 'rating')), True)]
    elif (recvr != 0 and recvr != 99) and chance[0][0] == 'thru':
        if len(chance) == 1:
            return ['thruside', recvr, misc.ranpow(3, int(pid2bute(offlineup[passr], 'rating'))) * misc.ranpow(1, int(pid2bute(offlineup[recvr], 'rating')))]
        elif len(chance) == 2:
            if recvr == passr:
                return ['dribble', recvr, misc.ranpow(1.75, int(pid2bute(offlineup[passr], 'rating')))]
            elif recvr == side(passr):
                return ['precross', recvr, misc.ranpow(0.25, int(pid2bute(offlineup[passr], 'rating')))]
            else:
                if random.random() > (0.85) ** (len(chance) - 1):
                    return ['keypass', recvr,misc.ranpow(1.5, int(pid2bute(offlineup[passr], 'rating')))]
                else:
                    return ['short', recvr,misc.ranpow(0.25, int(pid2bute(offlineup[passr], 'rating')))]
        else:
            if chance[-1][0] == 'dribble' or chance[-1][0] == 'keypass':
                return ['cutback', recvr, misc.ranpow(1, int(pid2bute(offlineup[passr], 'rating')))]
            else:
                if random.random() > (0.85) ** (len(chance) - 1):
                    return ['keypass', recvr,misc.ranpow(1.5, int(pid2bute(offlineup[passr], 'rating')))]
                else:
                    return ['short', recvr,misc.ranpow(0.25, int(pid2bute(offlineup[passr], 'rating')))]
    elif recvr == 0:
        return ['shot', passr, misc.ranpow(2, int(pid2bute(offlineup[passr], 'rating')), True)]
    else:
        return ['finish', passr, misc.ranpow(1, int(pid2bute(offlineup[passr], 'rating')), True)]


def defender():
    return [2, 3, 4, 5, 'DM', 6, 8]

def badpassresult(chance, place):
    if chance[place][0] == 'cutback' and random.random() < 0.5:
        return 'corner'
    if chance[place][0] == 'short' and random.random() < 0.08:
    	return 'ballback'
    if chance[place][0] == 'short' and random.random() < 0.08:
        return 'corner' 
    if chance[place][0] == 'cross' and random.random() < 0.4:
        return 'corner'
    if chance[place][0] == 'precross' and random.random() < 0.03:
        return 'ballback'
    if chance[place][0] == 'dribble' and random.random() < 0.05:
        return 'ballback'
    return 'turnover'

def foul(chance, place):
    if chance[place][0] == 'cutback' and random.random() < 0.01:
        return 'penalty'
    if (chance[place][0] == 'short' or chance[place][0] == 'precross') and random.random() < 0.025:
        return 'setpiece' 
    if chance[place][0] == 'cross' and random.random() < 0.002:
        return 'penalty'
    if chance[place][0] == 'keypass' and random.random() < 0.035:
        return 'penalty'
    if chance[place][0] == 'dribble' and random.random() < 0.175:
        if place > 3:
            return 'penalty'
        else:
            return 'setpiece'
    return 'no'

def poscounter(chance, place):
    o = counterattackers()
    d = counterdefenders()
    if random.random() < 0.5:
        return "counter " + d + " , " + o
    else:
        return "boring"

def pid2bute(pid, attribute):
    with open('players.csv') as File:
        reader = csv.DictReader(File)
        for player in reader:
            if pid == player.get('pid'):
                return player.get(attribute)


def findchance(ball, formation, nextplay):
    global offlineup
    global deflineup
    global setpieces
    global poss
    chance = list()
    if nextplay == 'tramp':
        x=random.choice([2, 5, 6, 7, 8, 9,9,9,9,9,9,9,9,9,9, 10, 11])
        if random.random() > 0.4:
            chance = [['tramp', x, 1], ['shot', x, misc.ranpow(1, int(pid2bute(offlineup[x], 'rating')))]]
    if nextplay == 'corner':
        chance = setpiece(7, 9)
        events.append('cornerearned')
    elif nextplay == 'setpiece':
        where = random.choice([1, 6, 6, 5, 5, 4])
        if where == 1:
            x = random.random()/20 + misc.ranB(0.025, int(pid2bute(offlineup[setpieces[poss][0]], 'rating')), True)
            if x > (0.25/8):
                chance = [['deadball', setpieces[poss][0], 1],['freekick', setpieces[poss][0], 1],['shot', setpieces[poss][0], x]]
            else:
                chance = setpiece(4, 6, 0.25)
        else:
            chance = setpiece(5, 8, (where/20))
    elif nextplay == 'penalty':
        chance = [['deadball', setpieces[poss][0], 1],['penalty', setpieces[poss][0], 1],['shot', setpieces[poss][0], misc.ranB(0.76, int(pid2bute(offlineup[setpieces[poss][0]], 'rating')))]]
        events.append('penearned')
        #print(chance)
        #print(len(chance))
    if chance == list():
        whothere = [[],[]]
        if 'counter' in nextplay:
            words = nextplay.split()
            chance = [['counter', ball, 1]]
            if len(words) == 3:
                #print(setpieces)
                #print(setpieces[poss])
                #adds players to counterattack if corner kick
                for player in range(9):
                    #print(setpieces[poss][9-player])
                    if int(words[1]) > player:
                        whothere[0].append(int(setpieces[poss][9-player]))
                    elif misc.ranB(0.25, int(pid2bute(offlineup[setpieces[poss][9-player]], 'rating'))) > random.random() and int(setpieces[poss][9-player]) in attackers():
                        whothere[0].append(int(setpieces[poss][9-player]))
                    if int(words[2]) > player:
                        whothere[1].append(int(setpieces[1-poss][9-player]))
                    elif misc.ranB(0.15, int(pid2bute(offlineup[setpieces[1-poss][9-player]], 'rating'))) > random.random() and not int(setpieces[1-poss][9-player]) in attackers():
                        whothere[0].append(int(setpieces[1-poss][9-player]))
            else:
                comma = False
                for word in words:
                    if word == ',':
                        comma = True
                        continue
                    elif word == 'counter':
                        continue
                    else:
                        if comma:
                            whothere[0].append(int(word))
                        else:
                            whothere[1].append(int(word))
            if len(whothere[0]) < 2:
                    chance = [[random.choice(['sequence','thrumid', 'thru']), ball, 1]]
                    whothere = list()            
        else:
            chance = [[random.choice(['sequence','thrumid', 'thru']), ball, 1]]
        #print(chance)
        while (chance[-1][0] != 'shot' and chance[-1][0] != 'finish'):
            #print(whothere)
            chance.append(nex(chance, whothere))
            #print(chance)
    #print(chance)
    return chance

def alterchance(chance, place, newidea):
    newchanc = []
    for play in chance:
        if place >= 1:
            newchanc.append(play)
            place -= 1
        elif place == 0:
            newchanc.append(['pre'+newidea, play[1], play[2]])
            break
    while (chance[-1][0] != 'shot' and chance[-1][0] != 'finish'):
        newchanc.append(nex(chance))
    return newchanc

        


def turnover():
    global poss
    global offlineup
    global deflineup
    global homelineup
    global awaylineup
    poss = 1 - poss
    if poss == 1:
        offlineup = awaylineup
        deflineup = homelineup
    else:
        offlineup = homelineup
        deflineup = awaylineup
    return random.choice([2, 3, 4, 5, 6, 8])


def game(home, away, league):
    global poss
    global offlineup
    global deflineup
    global homelineup
    global awaylineup
    global minute
    global setpieces
    global events
    awaylineup = []
    homelineup = []
    offlineup = []
    deflineup = []
    poss = 0
    events = []
    rosters = misc.find('sock')
    for team in rosters:
        if home == team["team"]:
            homelineup.append(team['formation'])
        if away == team['team']:
            awaylineup.append(team['formation'])
    for x in range(11):
        for team in rosters:
            if home == team["team"]:
                homelineup.append(team[str(x + 1)])
            if away == team['team']:
                awaylineup.append(team[str(x + 1)])
    setpieces = misc.setpieces(homelineup, awaylineup)
    goals = []
    minute = 0
    second = 0
    GS = [0, 0, home, away]
    offlineup = homelineup
    deflineup = awaylineup
    ball = random.choice([2, 3, 4, 5, 6, 8])
    nextplay = 'Afternoon De Ligt'
    while (minute < 96) and (len(goals) < 15):
        while second < 60:
            #print(nextplay)
            chance = findchance(ball, offlineup[0], nextplay)
            #print(chance)
            nextplay = 'boring'
            #chance = [['sequence', 2, 1],['pass', 3, 1],['pass', 6, 1],['pass', 10, 1],['keypass', 11, 1],['shot', 9, 1]]
            #chance = [['thrumid', 2, 1],['thruongoal', 3, 1],['shot', 6, 1]]
            place = 0
            while len(chance) > (place+1) and chance[place][0] != 'shot':
                second += 3
                #print(chance[0][0])
                if (chance[0][0] == 'sequence' and misc.dothesequence(chance,place)) or (chance[0][0] == 'thrumid' and chance[1][2] > 0.02) or (chance[0][0] == 'thru' and misc.dothethru(chance,place)) or chance[0][0] == 'setpiece' or chance[0][0] == 'corner' or (chance[0][0] == 'counter' and misc.dothecounter(chance, place))or chance[0][0] == 'penalty' or chance[0][0] == 'freekick' or chance[0][0] == 'tramp' or chance[0][0] == 'deadball':
                    #print(place)
                    #print(chance)
                    if chance[place][2] > random.random():
                        #print('completed')
                        nextplay=foul(chance, place)
                        if nextplay == 'no':
                            place += 1
                        else:
                            chance = []
                        #print('completeded')
                    else:
                        #print('interception')
                        nextplay = badpassresult(chance, place)
                        if x == 'ballback':
                            continue
                        else:
                            chance = []
                            nextplay = poscounter(chance, place)
                            ball = turnover()
                elif chance[0][0] == 'sequence' and place > 5:
                    chance = alterchance(chance, place, 'dribble')
                    #print(chance)
                elif chance[0][0] == 'sequence' and place > 3:
                    chance = alterchance(chance, place, 'cross')
                    #print(chance)
                else:
                    #print('passback')
                    chance = []
            if len(chance) == (place+1):
                if (chance[place][0] == 'shot') or (chance[place][0] == 'finish'):
                    #take shot
                    second += 3
                    events.append('shottaken')
                    x = random.random()
                    #print(x)
                    if chance[place][2] > x:
                        second += 3
                        #goal is scored
                        goals.append(roal(chance))
                        GS[poss] += 1
                        ball = turnover()
                        print(chance)
                    elif chance[place][2] + 0.05 > x:
                        nextplay = 'tramp'
                    elif chance[place][2] + 0.2 > x:
                        nextplay = 'corner'
                        #corner kick
                    else:
                        ball = turnover()
                elif chance[place][0] == 'clearance':
                    if chance[place][2] > random.random():
                        ball = turnover()
                        nextplay = 'counter ' + chance[place][1]

        second -= 60
        minute += 1
        #nextplay = 'counter 7 9'

    #adjust table
    if league:
        table = []
        with open('table.csv') as File:
            reader = csv.DictReader(File)
            for row in reader:
                table.append(row)
        for team in table:
            team['W'] = int(team['W'])
            team['L'] = int(team['L'])
            team['D'] = int(team['D'])
            team['GA'] = int(team['GA'])
            team['GS'] = int(team['GS'])
            team['GD'] = int(team['GD'])
            team['points'] = int(team['points'])
            if team['team'] == home:
                if GS[0] > GS[1]:
                    team['W'] += 1
                    team['points'] += 3
                elif GS[0] < GS[1]:
                    team['L'] += 1
                else:
                    team['D'] += 1
                    team['points'] += 1
                team['GA'] += GS[1]
                team['GS'] += GS[0]
                team['GD'] += (GS[0] - GS[1])
            if team['team'] == away:
                if GS[1] > GS[0]:
                    team['W'] += 1
                    team['points'] += 3
                elif GS[1] < GS[0]:
                    team['L'] += 1
                else:
                    team['D'] += 1
                    team['points'] += 1
                team['GA'] += GS[0]
                team['GS'] += GS[1]
                team['GD'] += (GS[1] - GS[0])
        with open('table.csv', 'w') as csvfile:
            fieldnames = ['team', 'W', 'D', 'L', 'GS', 'GA', 'GD', 'points']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(table)

    players = misc.find('players')
    for goal in goals:
        words = goal.split()
        assist = False
        if len(words) > 4:
            assist = True
        for player in players:
            if words[0] == player['playername']:
                player['goals'] = int(player['goals']) + 1
            if assist == True:
                if words[4] == player['playername']:
                    player['assists'] = int(player['assists']) + 1
    misc.rewrite('players',
                 ['playername', 'rating', 'pid', 'goals', 'assists'], players)

    misc.updateseq(goals, events)

    return [goals, GS, events]
