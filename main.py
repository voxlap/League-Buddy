import discord
import nltk
import requests
from PIL import Image
import requests
from io import BytesIO

base_url = 'https://na1.api.riotgames.com/lol/'
with open('Lolkey.txt', 'r+') as myfile:
    LoLkey = str(myfile.read())
summoners = {}
summonerMatches = {}
champEmojis = {}
client = discord.Client()
summonerRegion = {}
with open('discordToken.txt', 'r+') as myfile:
    token = str(myfile.read())

#################################
#           MESSAGES            #
#################################

    
def summonerStats(discordUser, userID):
    league = requests.get('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/'+ str(summoners[discordUser]['id']) + '?api_key=' + LoLkey).json()[0]
    regionCode = 'NA'
    embed=discord.Embed(title='**Summoner Profile: ' + summoners[discordUser]['name'] +'**', color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    embed.add_field(name='Summoner Level', value=summoners[discordUser]['summonerLevel'], inline=False)
    embed.add_field(name='Rank', value=league['tier'] + ' ' + league['rank'] + ', ' + str(league['wins']) + 'W/' + str(league['losses']) + 'L', inline=True)
    embed.add_field(name='Region', value=regionCode, inline=True)

    return embed

def lastMatchMessage(DISCORD_USER, server, userID, match):
    teamID = getTeam(match, summoners[DISCORD_USER]['accountId'])
    stats = getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId']))
    
    embed=discord.Embed(title='__**' + (summoners[DISCORD_USER]['name'] + '\'s Last Match Summary:**__'), description=('<@' + userID + '>' + ', here\'s a quick overview of that last match!'), color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[DISCORD_USER]['profileIconId']) + '.png')
    embed.add_field(name='Game Mode:', value= match['gameMode'][0].upper() + match['gameMode'].lower()[1:], inline=True)
    embed.add_field(name='Match Type:', value= match['gameType'][0].upper() + match['gameType'].lower()[1:], inline=True)
    embed.add_field(name='Win/Loss:', value=win_lose(match, summoners[DISCORD_USER]['accountId']), inline=False)
    embed.add_field(name='Champion Played:', value= (str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId']))))), inline=True)
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
    embed.set_footer(text='Thanks for using League-Buddy!')

    return embed

def lastMatchTeamMessage(match, teamID, userID):
    embed=discord.Embed(title='**Summoner\'s Team Performance:**', description='<@' + userID + '>' + '\'s team statistics during their last match', color=0x0ee796)
    embed.add_field(name='Kills', value=totalTeamKills(match, teamID), inline=True)
    embed.add_field(name='Deaths', value=totalTeamDeaths(match, teamID), inline=True)
    embed.add_field(name='Towers Killed', value=totalTeamTowerKills(match, teamID), inline=False)
    embed.add_field(name='Inhibitor Kills', value=totalTeamInhibitorKills(match, teamID), inline=True)
    embed.add_field(name='Dragons Killed', value=totalTeamDragonKills(match, teamID), inline=True)
    embed.add_field(name='Barons Killed', value=totalTeamBaronKills(match, teamID), inline=True)
    embed.add_field(name='Rift Herald Kills', value=totalTeamRiftHeraldKills(match, teamID), inline=True)
    embed.add_field(name='Vilemaws Killed', value=totalTeamVilemawKills(match, teamID), inline=True)

    return embed

def registerMessage(discordUser, userID):
    embed=discord.Embed(description='<@' + userID + '>' + ' Registered with League-Buddy as level ' + str(summoners[discordUser]['summonerLevel']) + ' summoner.', color=0x0ee796)
    embed.set_author(name=summoners[discordUser]['name'],icon_url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    return embed

def changeSummonerMessage(discordUser, userID):
    embed=discord.Embed(description='<@' + userID + '>' + ' League-Buddy summoner changed', color=0x0ee796)
    embed.set_author(name=summoners[discordUser]['name'],icon_url='http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    return embed

#################################
#           TEAM                #
#################################


def totalTeamKills(match, teamID):
    kills = 0
    for i in range(len(match['participants'])):
        if match['participants'][i]['teamId'] == teamID:
            kills += match['participants'][i]['stats']['kills']
    return kills
                        
def totalTeamDeaths(match, teamID):
    deaths = 0
    for i in range(len(match['participants'])):
        if match['participants'][i]['teamId'] == teamID:
            deaths += match['participants'][i]['stats']['deaths']
    return deaths
                        
def totalTeamTowerKills(match, teamID):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['towerKills']
                        
def totalTeamInhibitorKills(match, teamID):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['inhibitorKills']
                        
def totalTeamDragonKills(match, teamID):
   for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['dragonKills']
            
def totalTeamBaronKills(match, teamID):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['baronKills']
                        
def totalTeamRiftHeraldKills(match, teamID):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['riftHeraldKills']
                        
def totalTeamVilemawKills(match, teamID):
    for i in range(len(match['teams'])):
        if match['teams'][i]['teamId'] == teamID:
            return match['teams'][i]['vilemawKills']

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
        
def getTeamResults(match):
    return match['teams']

#################################
#           MATCH               #
#################################

def getLastMatch(account_id):
    match = requests.get(base_url + 'match/v3/matches/' + str((requests.get(base_url + 'match/v3/matchlists/by-account/'
                        + account_id + '/recent?api_key=' + LoLkey).json()['matches'][0]['gameId']))
                        + '/?api_key=' + LoLkey).json()
    addSummonerMatch(account_id, match)
    return match

def addSummonerMatch(account_id, match):
    if account_id not in summonerMatches.keys():
        summonerMatches[account_id] = []
        summonerMatches[account_id].append(match)
        return
    summonerMatches[account_id].append(match)
    return

def compareLastMatch(match):
    return

def getChampName(champID):
    message = requests.get(base_url + 'static-data/v3/champions/' + champID + '?locale=en_US&api_key=' + LoLkey).json()
    return message['name']

def getSummonerChamp(match, accountId):
    userChamp = str()
    for i in range(len(match['participants'])):
        if match['participants'][i]['participantId'] == getParticipantID(match, accountId):
            userChamp = match['participants'][i]['championId']
    return userChamp

def compareKDA(KDA1, KDA2):
    return

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


def changeSummoner(summoner, discordID):
    summoners[discordID] = summoner 
    print(summoners)

def getSummoner(summonerName):
    summoner = requests.get(base_url + 'summoner/v3/summoners/by-name/'+ summonerName + '?api_key=' + LoLkey).json()
    return summoner

def registerSummoner(summoner, discordID):
    if discordID not in summoners:
        summoners[discordID] = summoner 
    print(summoners)
    
def getParticipantStats(match, participantID):
    return match['participants'][participantID - 1]['stats']

def getParticipantKDA(stats):
    message = str(stats['kills']) + '/' + str(stats['deaths']) + '/' + str(stats['assists'])
    return message
	
def getParticipantID(match, accountID):
    message = str()
    for j in range(len(match['participantIdentities'])):
        if match['participantIdentities'][j]['player']['accountId'] == accountID:
            return match['participantIdentities'][j]['participantId']

##############################################################################

def champEmoji(server, userChamp):
    if userChamp not in champEmojis.keys():
        return makeChampionEmoji(server, userChamp)
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>' 

def makeChampionEmoji(server, userChamp):
    url = str('http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + str(userChamp) + '.png')
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    server.create_custom_emoji(server=server, name=userChamp, image=img)
    print(server.emojis)
    champEmojis[userChamp] = server.emojis
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>'

def messageTokenizor(message):
    tokens = nltk.word_tokenize(message)
    return tokens


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
    if message.content.startswith('!lb last match report'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, embed=lastMatchMessage(str(message.author), message.server, str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']))))
        #await client.send_message(message.channel, lastMatchMessage(str(message.author), str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']))))
    if message.content.startswith('!lb last match team'):
        accountID = str(summoners[str(message.author)]['accountId'])
        match = getLastMatch(accountID)
        teamID = getTeam(match, summoners[str(message.author)]['accountId'])
        await client.send_message(message.channel, embed=lastMatchTeamMessage(match, teamID, message.author.id))
    if message.content.startswith('!lb register'):
        text = messageTokenizor(message.content)
        registerSummoner(getSummoner(text[3]), str(message.author))
        await client.send_message(message.channel, embed=registerMessage(str(message.author), str(message.author.id)))
    if message.content.startswith('!lb summoner'):
        await client.send_message(message.channel, embed=summonerStats(str(message.author), str(message.author.id)))
    if message.content.startswith('!lb change summoner'):
        text = messageTokenizor(message.content)
        changeSummoner(getSummoner(text[4]), str(message.author))
        await client.send_message(message.channel, embed=changeSummonerMessage(str(message.author), str(message.author.id)))
#Discord Bot Authentication data
client.run(token)
