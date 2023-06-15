import discord
import os
import random
import time
import csv
import math
final = []
def rewrite(tabel, fieldnames,table):
  with open(tabel + '.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(table)

def find(tabel):
	table = []
	with open(tabel + '.csv') as File:
		reader = csv.DictReader(File)
		for row in reader:
			table.append(row)
	return table

def form(formation):
    if formation == '4231':
        return [2,3,4,5,'DM',6,8,'M','AM',7,10,11,'ST',9]

def setpieces(homeline, awayline):
	return [[10,4,3,9,8,7,6,11,2,5],[10,4,3,9,8,7,6,11,2,5]]

def tts(ist):
    rme = ''
    for item in ist:
        rme = rme + ' ' + str(item)
    return rme


def cleartable():
		table = []
		with open('table.csv') as File:
			reader = csv.DictReader(File)
			for row in reader:
				table.append(row)
		for team in table:
			team['W'] = 0
			team['L'] = 0
			team['D'] = 0
			team['GA'] = 0
			team['GS'] = 0
			team['GD'] = 0
			team['points'] = 0
			team['rank'] = 0
			team.pop('rank')
		fieldnames = ['team', 'W', 'D', 'L', 'GS', 'GA', 'GD','points']
		rewrite('table',fieldnames,table)
	 
def sort(tabel, cat):
	table = find(tabel)
	for team in table:
		team['rank'] = 1
		for o in table:
			if int(o[cat]) > int(team[cat]):
				team['rank'] += 1
	newtable = []
	for x in range(len(table)):
		for team in table:
			if team['rank'] == x + 1:
				newtable.append(team)
	rewrite(tabel, newtable[0].keys(), newtable)
	return newtable

def ranpow(exponent,rating = 50, offense = True):
	rme=ranB(random.random(),rating, offense) ** (exponent % 1)
	for x in range(math.floor(exponent)):
		rme*=ranB(random.random(),rating,offense)
	return rme

def bell(multiplier = 1, sdadj = 1):
	return ((ranpow(2) - ranpow(2) + 1)/sdadj + ((sdadj-1)/sdadj)) *(multiplier/2)

def ranB(prob, rating=50, offense = True):
	rating /= 50
	if offense:
		rating = 2-rating
	if rating > 1:
		x=(prob ** rating)
	else:
		x= (1-((1-prob) ** (2-rating)))
	return x

def sequence(chance):
    '''
    if chance[-2][0] == 'cross':
        return ' by a beautiful cross that was masterfully crafted.'
    elif chance[-2][0] == 'cutback':
        return ' who found the cutback after taking it in.'
    elif chance[0][0] == 'thru':
        return ' directly following a wide run creating the chance.'
    elif chance[0][0] == 'sequence':
        return ' after a brilliant sequence of short quick passing.'
    elif chance[0][0] == 'thrumid':
        return ' via a gorgeous through ball over the defence.'
    elif chance[0][0] == 'corner':
        return ' coming off a corner kick perfectly executed.'
    elif chance[0][0] == 'penalty':
        return ' completing the perfectly placed precise penalty Penaldo would be proud of.'
    elif chance[0][0] == 'freekick':
        return ' ON A BENT LIKE BECKHAM FREEKICK SUIIIIIIIIII.'
    elif chance[0][0] == 'setpiece':
        return ' reslting from a set peice well created.'
    elif chance[0][0] == 'counter':
        return ' finishing the clean counter after much anticipation.'
    elif chance[0][0] == 'tramp':
        return ' cleaning the mess with a tramp goal.'
    else:
        return '.  I don\'t even know how to explain it!'
        '''
    return ' ' + chance[0][0] + ' ' + chance[-2][0] + ' '+ chance[-1][0]

def updateseq(goals, events):
    sqct = find('seqcount')
    #print(sqct)
    sqct[-1]['total'] = int(sqct[-1]['total']) + 1
    for goal in goals:
        sqct[-2]['total'] = int(sqct[-2]['total']) + 1
        words = goal.split()
        for typ in sqct:
            if typ['type'] == words[-1]:
                typ['total'] = int(typ['total']) + 1
            if typ['type'] == words[-2]:
                typ['total'] = int(typ['total']) + 1
            if typ['type'] == words[-3]:
                typ['total'] = int(typ['total']) + 1
    for event in events:
        for typ in sqct:
            if typ['type'] == event:
                typ['total'] = int(typ['total']) + 1
    for typ in sqct:
        typ['pergame'] = (int(typ['total']) / int(sqct[-1]['total']))
        if len(goals) > 0: 
            typ['percentage'] = (int(typ['total']) / int(sqct[-2]['total']))
        rewrite('seqcount', ['type', 'total', 'pergame', 'percentage'], sqct)

def clearseq():
	sqct = find('seqcount')
	for typ in sqct:
		typ['total'] = 0
		typ['pergame'] = 0
		typ['percentage'] = 0
	rewrite('seqcount', ['type', 'total', 'pergame', 'percentage'], sqct)

def dothethru(chance,place):
	if place == 1:
		return (chance[1][2] > 0.1)
	elif chance[place][0] == 'short':
		return ((chance[place][2] * chance[place+1][2]) > 0.6)
	else:
		return True

def dothesequence(chance,place):
    keyplace = 0
    for play in range(len(chance)):
        if chance[play][0] == 'keypass' or chance[play][0] == 'dribble':
            keyplace = play
    if place >= keyplace:
        return (chance[place][2] > 0.005)
    else:
        return ((chance[place][2] * chance[place+1][2]) > 0.6)

def dothecounter(chance,place):
    keyplace = 0
    for play in range(len(chance)):
        if chance[play][0] == 'shot':
            keyplace = play
    if place-1 >= keyplace:
        return (chance[place][2] > 0.05)
    else:
        return ((chance[place][2] * chance[place+1][2]) > 0.2)

def schedule(teams):
    global final
    #print(teams)
    numteams = len(teams)
    if len(teams) == 1 or isinstance(teams, str):
        return []
    else:
        x = split(teams)
    #print(x)
    sch = [[schedule(x[0]),schedule(x[1]),schedule(x[2]),schedule(x[3])],[versus(x[0],x[1]),
    versus(x[2],x[3])],
    [versus(x[0],x[2], False),
    versus(x[1],x[3], False)],
    [versus(x[3],x[0]),
    versus(x[1],x[2])]]
    #print(sch)
    final = []
    delist(sch)
    #print(sch)
    z = []
    for match in final:
        if not(match[0] == 'bye' or match[1] == 'bye'):
            z.append(match)
    #print(z)
    final = []
    #print(numteams)
    perweek = math.floor(numteams/2)
    #print(perweek)
    left = list(range(len(z)))
    #print(len(z)/perweek)
    if 1==3:
        print('noon mensch')
    else:
        for weeknum in range(int(len(z)/perweek)):
            week = []
            reverse = True
            #repeat however many times needed
            for gamenumthisweek in range(perweek):
                #repeat until i find one that works
                for match in left:
                    okay = True
                    for sett in week:
                        if ((z[match][0] == sett[0]) or (z[match][0] == sett[1]) or (z[match][1] == sett[0]) or (z[match][1] == sett[1])):
                            okay = False
                    if okay:
                        it = match
                        break
                if not okay:
                    for match in week:
                        week.remove(match)
                        final.remove(match)
                    if reverse:
                        z.reverse()
                        reverse = False
                    else:
                        random.shuffle(z)
                    left = list(range(len(z)))
                week.append(z[it])
                final.append(z[it])
                left.remove(it)
            #print(week)
            #print(final)
    #print(final)
    return final
        
def versus(team1, team2, fix = True):
    rme = []
    if isinstance(team1, str):
        if fix or random.random() > 0.5:
            return [team1, team2]
        else:
            return [team2, team1]
    if len(team1) == 1:
        if fix or random.random() > 0.5:
            return [team1[0], team2[0]]
        else:
            return [team2[0], team1[0]]
    else:
        rme.append([versus(team1[0], team2[0]), versus(team1[1], team2[1]), versus(team1[2], team2[2]), versus(team1[3], team2[3])])
        rme.append([versus(team2[0], team1[1]), versus(team2[1], team1[2]), versus(team2[2], team1[3]), versus(team2[3], team1[0])])
        rme.append([versus(team1[0], team2[2]), versus(team1[1], team2[3]), versus(team1[2], team2[0]), versus(team1[3], team2[1])])
        rme.append([versus(team2[0], team1[3]), versus(team2[1], team1[0]), versus(team2[2], team1[1]), versus(team2[3], team1[2])])
    return rme

def split(teams):
    x = len(teams)
    y = 0
    a = []
    b = []
    c = []
    d = []
    if x > 1:
        if x%4 != 0:
            for i in range(4-(x%4)):
                teams.append('bye')
        while x>0:
            a.append(teams[0+y])
            b.append(teams[1+y])
            c.append(teams[2+y])
            d.append(teams[3+y])
            x-=4
            y+=4
        if len(a) == 1:
            return [a[0],b[0],c[0],d[0]]
        else:
            return [a,b,c,d]
    else:
        return teams
    
def delist(ist):
    global final
    for st in ist:
        if len(st) > 0:
            if isinstance(st[0], str):
                final.append(st)
            else:
                delist(st)


    