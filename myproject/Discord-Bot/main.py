import discord
import os
import random
import time
import csv
import engine
import misc
import statistics

client = discord.Client()
oouser = []
oochal = "ligma balls"
oonum = 0
oonum2 = 0
mbappe_triggers = [
    'kylian', 'mbappe', 'bruno', 'pen', 'neymar', 'france', 'euro', 'pogba',
    'kante', 'greizmann', 'shoot', 'goal', 'goals', 'world', 'cup',
    'Kylian', 'Mbappe', 'Bruno', 'Pen', 'Neymar', 'France', 'Euro', 'Pogba',
    'Kante', 'Greizmann', 'Shoot', 'Goal', 'Goals', 'World', 'Cup',
    'german', 'German', 'Ital', 'Swi', 'kick', 'Kick', 'mbotppe', 'Mbotppe',
    'MBotppe'
]
rosters = []
with open('sock.csv') as File:
    reader = csv.DictReader(File)
    for row in reader:
        rosters.append(row)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	words = message.content.split()

	global oonum
	global oouser
	global oochal
	global oonum2
	global rosters

	if message.author == client.user:
		return

	if any(word in message.content for word in mbappe_triggers):
		await message.channel.send('https://tenor.com/view/mbappe-swiss-switzerland-miss-penalty-gif-22146850')

	if (('its coming home' in message.content) or ('it\'s coming home' in message.content)) and str(message.author) == "jimmyboi#7459":
			await message.channel.send( 'https://tenor.com/view/cry-about-it-england-rashford-saka-italy-gif-22304969')
			await message.channel.send("Shut the fuck up Jim.  It's not coming home.")

	if message.content.startswith("~soccer"):
		print("The game has begun")
		gameinfo = engine.game(words[1], words[2], False)
		for goal in gameinfo[0]:
			print(goal)
		GS = gameinfo[1]
		print(GS[2] + " " + str(GS[0]) + ", " + GS[3] + " " +str(GS[1]))

	if message.content.startswith("~team"):
		players = misc.find('players')
		for player in players:
			player['assists'] = 0
		misc.rewrite('players', ['playername','rating','pid','goals','assists'], players)

	if ('your mom' in message.content or 'ur mom' in message.content or 'ur mum' in message.content) and str(message.author) == "JUJU3P#6361":
		await message.channel.send("Hilarious and original, julien.")
	elif ('your mom' in message.content or 'ur mom' in message.content or 'ur mum' in message.content):
		artur = message.author
		await message.channel.send("Hilarious and original, " + str(artur))

	if ('valorant' in message.content or "Valorant" in message.content) and str(message.author) == "Nubbin#0001":
		await message.channel.send("https://tenor.com/view/sweating-wet-wipe-gif-15394859")

	if message.content.startswith('~cleartable'):
		misc.cleartable()
		misc.clearseq()

    
	if message.content.startswith('~season'):
		misc.cleartable()
		if 'clear' in words:
			misc.clearseq()
		table = misc.find('table')
		printresults = False
		if 'result' in words:
			printresults = True
		if len(words) == 1:
			words.append('1')
		for x in range(int(words[1])):
			teams = []
			for team in table:
				teams.append(team['team'])
			schedule = misc.schedule(teams)
			for game in schedule:
						gameinfo = engine.game(game[0], game[1], True)
						for goal in gameinfo[0]:
							print(goal)
						GS = (gameinfo[1]) 
						print(GS[2] + " " + str(GS[0]) + ", " + GS[3] + " " +str(GS[1]))
		table = misc.sort('table', 'points')
		if printresults:
			for team in table:
		   		await message.channel.send(team['team'] + " " + team['points'])
		else:
			for team in table:
		   		print(team['team'] + " " + team['points'])

	if message.content.startswith('~schedule'):
		table = misc.find('table')
		teams = []
		for team in table:
			teams.append(team['team'])
		random.shuffle(teams)
		print(misc.schedule(teams))


	if message.content.startswith('~verdict'):
		if random.random() > 0.5:
			await message.channel.send('guilty')
		else:
			await message.channel.send('innocent')


client.run(os.getenv('TOKEN'))
