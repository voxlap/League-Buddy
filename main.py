import discord
import nltk
import requests

base_url = 'https://na1.api.riotgames.com/lol/'
LoLkey = 'RGAPI-bad08388-070d-4b8f-b726-f648ff6930d8'
global summoners
summoners = {}
summonerMatches = {}
champEmojis = {}
client = discord.Client()

def lastMatchMessage(DISCORD_USER, server, userID, match):
    teamID = getTeam(match, summoners[DISCORD_USER]['accountId'])
    stats = getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId']))
    
    embed=discord.Embed(title='__**' + (summoners[DISCORD_USER]['name'] + '\'s Last Match Summary:**__'), description=('<@' + userID + '>' + ', here\'s a quick overview of that last match!'), color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[DISCORD_USER]['profileIconId']) + '.png')
    embed.add_field(name='Game Mode:', value= match['gameMode'][0].upper() + match['gameMode'].lower()[1:], inline=True)
    embed.add_field(name='Match Type:', value= match['gameType'][0].upper() + match['gameType'].lower()[1:], inline=True)
    embed.add_field(name='Win/Loss:', value=win_lose(match, summoners[DISCORD_USER]['accountId']), inline=False)
    print(str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId'])))))
    embed.add_field(name='Champion Played:', value=(champEmoji(server, str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId']))))) + str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId']))))), inline=True)
    embed.add_field(name='Champion Level Reached:', value=str(stats['champLevel']), inline=True)
    embed.add_field(name='K/D/A:', value=str(getParticipantKDA(getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId'])))), inline=False)
    embed.add_field(name='CS:', value=str(stats['totalMinionsKilled']), inline=True)
    embed.add_field(name='Total Damage Dealt:', value=str(stats['totalDamageDealt']), inline=True)
    embed.add_field(name='Turrets Killed:', value=str(stats['turretKills']), inline=True)
    embed.add_field(name='Inhibitors Killed', value=str(stats['inhibitorKills']), inline=True)
    embed.add_field(name='Double Kills:', value=str(stats['doubleKills']), inline=True)
    embed.add_field(name='Triple Kills:', value=str(stats['tripleKills']), inline=True)
    embed.add_field(name='Quadra Kills:', value=str(stats['quadraKills']), inline=True)
    embed.add_field(name='Penta Kills:', value=str(stats['pentaKills']), inline=True)
    embed.add_field(name='Unreal Kills:', value=str(stats['unrealKills']), inline=True)
    embed.set_footer(text="Thanks for using League-Buddy!")

    return embed
    
'''    
    message = ('<@' + userID + '>' + ' \'s last match was a ' + match['gameMode'].lower() + ' match. '
               + '<@' + userID + '>' + ' played as ' + str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId'])))) + ', and'
               + win_lose(match, summoners[DISCORD_USER]['accountId']) + '. Their champion reached level ' + str(stats['champLevel']) + ', earned '
               + str(stats['goldEarned']) + ' gold, had a CS of ' + str(stats['totalMinionsKilled']) + ', dealt ' + str(stats['totalDamageDealt'])
               + ' damage, killed ' + str(stats['turretKills']) + ' turrets, killed ' + str(stats['inhibitorKills']) + ' inhibitors, achieved '
               + str(stats['doubleKills']) + ' double kills, ' + str(stats['tripleKills']) + ' triple kills, ' + str(stats['quadraKills'])
               + ' quadra kills, ' + str(stats['pentaKills']) + ' penta kills, and ' + str(stats['unrealKills']) + ' unreal kills. Their KDA was '
               + str(getParticipantKDA(getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId'])))) + '. '
               + DISCORD_USER[0].upper() + DISCORD_USER[1:-5] + '\'s team' + str(gotFirstTower(teamID, match))
               + grammar2(gotFirstTower(teamID, match), gotFirstBlood(teamID, match)) + gotFirstBlood(teamID, match) + '.') 
    return message
'''



def champEmoji(server, userChamp):
    if userChamp not in champEmojis.keys():
        return makeChampionEmoji(server, userChamp)
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>' 

def makeChampionEmoji(server, userChamp):
    url = str('http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + str(userChamp) + '.png')
    print(url)
    
    client.create_custom_emoji(server=server, name=userChamp, image=url)
    print(server.emojis)
    champEmojis[userChamp] = server.emojis
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>'

def getLastMatch(account_id):
    match = requests.get(base_url + 'match/v3/matches/' + str((requests.get(base_url + 'match/v3/matchlists/by-account/'
                        + account_id + '/recent?api_key=' + LoLkey).json()['matches'][0]['gameId']))
                        + '/?api_key=' + LoLkey).json()
    addSummonerMatch(account_id, match)
    return match

def addSummonerMatch(account_id, match):
    summonerMatches[account_id] = []
    summonerMatches[account_id].append(match)
    
def getChampName(champID):
    message = requests.get(base_url + 'static-data/v3/champions/' + champID + '?locale=en_US&api_key=' + LoLkey).json()
    return message['name']

def getSummonerChamp(match, accountId):
    userChamp = str()
    for i in range(len(match['participants'])):
        if match['participants'][i]['participantId'] == getParticipantID(match, accountId):
            userChamp = match['participants'][i]['championId']
    return userChamp

def compareLastMatch(match):
    return

def compareKDA(KDA1, KDA2):
    return

def gotFirstTower(teamID, match):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            if match['teams'][i]['firstTower'] == True:
                return ' destroyed first tower'
            return ' did not destroy first tower'

def gotFirstBlood(teamID, match):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            if match['teams'][i]['firstBlood'] == True:
                return ' got first blood'
            return ' did not get first blood'

def getTeam(match, accountId):
    userTeam = str()
    for i in range(len(match['participants'])):
        if match['participants'][i]['participantId'] == getParticipantID(match, accountId):
            userTeam = match['participants'][i]['teamId']
    return userTeam

def win_lose(match, accountId):
    userTeam = getTeam(match, accountId)
    for i in range(len(match['teams'])):
        if userTeam == match['teams'][i]['teamId']:
            if match['teams'][i]['win'] == 'Fail':
                return ' Loss'
            return ' Win'

def getSummoner(summonerName):
    summoner = requests.get(base_url + 'summoner/v3/summoners/by-name/'+ summonerName + '?api_key=' + LoLkey).json()
    return summoner

def registerSummoner(summoner, discordID):
    if discordID not in summoners:
        summoners[discordID] = summoner 
    print(summoners)

def messageTokenizor(message):
    tokens = nltk.word_tokenize(message)
    return tokens
    
def getParticipantStats(match, participantID):
    return match['participants'][participantID - 1]['stats']

def getParticipantKDA(stats):
    message = str(stats['kills']) + '/' + str(stats['deaths']) + '/' + str(stats['assists'])
    return message
	
def getTeamResults(match):
    return match['teams']

def getParticipantID(match, accountID):
    message = str()
    for j in range(len(match['participantIdentities'])):
        if match['participantIdentities'][j]['player']['accountId'] == accountID:
            return match['participantIdentities'][j]['participantId']

def registerMessage(discordUser, userID):
    #message = '<@' + userID + '> registered with League Buddy as level ' + str(summoners[discordUser]['summonerLevel']) + ' summoner ' + str(summoners[discordUser]['name']) + '.'
    embed=discord.Embed(title='<@' + userID + '>' + ' Registered with League-Buddy as level ' + str(summoners[discordUser]['summonerLevel']) + ' summoner.', color=0x1cead6)
    embed.set_author(name=summoners[discordUser]['name'],icon_url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    return embed
def grammar2(firstTower, firstBlood):
	if 'not' in firstTower:
		if 'not' in firstBlood:
			return ' and'
		return ' but'
	return grammar(firstBlood)
	
def grammar(firstBlood):
    if 'not' in firstBlood:
        return ' but'
    return ' and'


@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await autoSetup()
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('!lastMatch'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, embed=lastMatchMessage(str(message.author), message.server, str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']))))
        #await client.send_message(message.channel, lastMatchMessage(str(message.author), str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']))))

    if message.content.startswith('!register'):
        text = messageTokenizor(message.content)
        registerSummoner(getSummoner(text[2]), str(message.author))
        await client.send_message(message.channel, embed=registerMessage(str(message.author), str(message.author.id)))
        
#Discord Bot Authentication data
client.run('NDE4NDE5NDc0MDM5OTYzNjYw.DXhTLg.BxfBe-w4fBriT0tLtY5IUcCZeTs')
