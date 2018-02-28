import discord
import nltk
import requests

base_url = 'https://na1.api.riotgames.com/lol/'
global summoners
summoners = {}
summonerMatches = {}

def lastMatchMessage(DISCORD_USER, userID, match):
    teamID = getTeam(match, summoners[DISCORD_USER]['accountId'])
    message = ('<@' + userID + '>' + ' \'s last match was a ' + match['gameMode'] + ' match. '
               + DISCORD_USER[:-5] + ' played as ' + str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId'])))) + ', and' + win_lose(match, summoners[DISCORD_USER]['accountId'])
               + '. Their KDA was ' + str(getParticipantKDA(getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId'])))) + '. '
               + DISCORD_USER[:-5] + '\'s team ' + str(gotFirstTower(teamID, match)) + grammar(gotFirstBlood(teamID, match)) + gotFirstBlood(teamID, match) + '.') 
    return message
def getLastMatch(account_id):
    match = requests.get(base_url + 'match/v3/matches/' + str((requests.get(base_url + 'match/v3/matchlists/by-account/'
                        + account_id + '/recent?api_key=RGAPI-5d68cc3e-483a-4be2-8e22-49563464bce1').json()['matches'][0]['gameId']))
                        + '/?api_key=RGAPI-5d68cc3e-483a-4be2-8e22-49563464bce1').json()
    addSummonerMatch(account_id, match)
    return match

def addSummonerMatch(account_id, match):
    summonerMatches[account_id] = []
    summonerMatches[account_id].append(match)


def getChampName(champID):
    message = requests.get(base_url + 'static-data/v3/champions/' + champID + '?locale=en_US&api_key=RGAPI-5d68cc3e-483a-4be2-8e22-49563464bce1').json()
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
        print(match['teams'][i]['teamId'])
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
                return ' lost'
            return ' win'
def getSummoner(summonerName):
    summoner = requests.get(base_url + 'summoner/v3/summoners/by-name/'+ summonerName + '?api_key=RGAPI-5d68cc3e-483a-4be2-8e22-49563464bce1').json()
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
    message = '<@' + userID + '> registered with League Buddy as level ' + str(summoners[discordUser]['summonerLevel']) + ' summoner ' + str(summoners[discordUser]['name']) + '.'
    return message

def grammar(firstBlood):
    if 'not' in firstBlood:
        return ' but'
    return ' and'
client = discord.Client()

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
        await client.send_message(message.channel, lastMatchMessage(str(message.author), str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']))))
    if message.content.startswith('!register'):
        text = messageTokenizor(message.content)
        registerSummoner(getSummoner(text[2]), str(message.author))
        await client.send_message(message.channel, registerMessage(str(message.author), str(message.author.id)))
        
#Discord Bot Authentication data
client.run('NDE4NDE5NDc0MDM5OTYzNjYw.DXhTLg.BxfBe-w4fBriT0tLtY5IUcCZeTs')
