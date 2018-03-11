import discord
import nltk
import requests
from PIL import Image
import requests
from io import BytesIO

base_url = '.api.riotgames.com/lol/'
validRegions = ['NA1', 'RU', 'KR', 'PBE1', 'BR1', 'OC1', 'JP1', 'EUN1', 'EUW1', 'TR1', 'LA1', 'LA2']
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


def registerRegion(discordUser, region):
    if region in validRegions:
        summonerRegion[discordUser] = region
        print(summonerRegion)
        return
    return "Not a valid region, try again"

def summonerStats(discordUser, userID):
    league = requests.get('https://' + str(summonerRegion[discordUser]) + '.api.riotgames.com/lol/league/v3/positions/by-summoner/'+ str(summoners[discordUser]['id']) + '?api_key=' + LoLkey).json()
    league = league[0]
    regionCode = summonerRegion[discordUser]
    embed=discord.Embed(title='**Summoner Profile: ' + summoners[discordUser]['name'] +'**', color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/8.5.2/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    embed.add_field(name='Summoner Level', value=summoners[discordUser]['summonerLevel'], inline=False)
    embed.add_field(name='League', value=league['leagueName'], inline=True)
    embed.add_field(name='LP', value=league['leaguePoints'], inline=True)
    embed.add_field(name='Rank in ' + league['queueType'], value=league['tier'] + ' ' + league['rank'] + ', ' + str(league['wins']) + 'W/' + str(league['losses']) + 'L', inline=True)
    embed.add_field(name='Region', value=regionCode, inline=True)
    return embed

def champMessage(champ):
    champData = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions/' + str(getChampID(champ)) + '?locale=en_US&champData=all&tags=all&api_key=' + LoLkey).json()
    embed=discord.Embed(title='**Champion: ' + champData['key'] + ' ' + champData['title'] +'**', color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/8.5.2/img/champion/' + champData['key'] + '.png')
    allyTips = ayallyTips(champData['allytips'])
    enemyTips = ayenemyTips(champData['enemytips'])
    embed.add_field(name='Ally Tips', value=allyTips, inline=False)
    embed.add_field(name='Enemy Tips', value=enemyTips, inline=False)
    embed.add_field(name='Attack Damage:', value=champData['stats']['attackdamage'], inline=True)
    embed.add_field(name='MP:', value=champData['stats']['mp'], inline=True)
    embed.add_field(name='HP:', value=champData['stats']['hp'], inline=True)
    embed.add_field(name='Armor:', value=champData['stats']['armor'], inline=True)
    embed.add_field(name='Movespeed:', value=champData['stats']['movespeed'], inline=True)
    embed.add_field(name='Attack Range:', value=champData['stats']['attackrange'], inline=True)
    return embed

def ayallyTips(tipList):
    message = str()
    for i in range(len(tipList)):
        message += ':small_blue_diamond: ' + tipList[i] + '\n'
    return message

def ayenemyTips(tipList):
    message = str()
    for i in range(len(tipList)):
        message += ':small_orange_diamond: ' + tipList[i] + '\n'
    return message


def lastMatchMessage(DISCORD_USER, server, userID, match):
    teamID = getTeam(match, summoners[DISCORD_USER]['accountId'])
    stats = getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId']))
    
    embed=discord.Embed(title='__**' + (summoners[DISCORD_USER]['name'] + '\'s Last Match Summary:**__'), description=('<@' + userID + '>' + ', here\'s a quick overview of that last match!'), color=0x0ee796)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/8.5.2/img/profileicon/' + str(summoners[DISCORD_USER]['profileIconId']) + '.png')
    embed.add_field(name='Game Mode:', value= match['gameMode'][0].upper() + match['gameMode'].lower()[1:], inline=True)
    embed.add_field(name='Match Type:', value= match['gameType'][0].upper() + match['gameType'].lower()[1:], inline=True)
    embed.add_field(name='Win/Loss:', value=win_lose(match, summoners[DISCORD_USER]['accountId']), inline=False)
    embed.add_field(name='Champion Played:', value= (str(getEmoji(str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId'])), DISCORD_USER)))) + ' ' + str(getChampName(str(getSummonerChamp(match, summoners[DISCORD_USER]['accountId'])), DISCORD_USER))), inline=True) 
    embed.add_field(name='Champion Level Reached:', value=str(stats['champLevel']), inline=True)
    embed.add_field(name='K/D/A:', value=str(getParticipantKDA(getParticipantStats(match, getParticipantID(match, summoners[DISCORD_USER]['accountId'])))), inline=False)
    embed.add_field(name='CS:', value='<:minion:421856483681107980>'+ ' ' + str(stats['totalMinionsKilled']), inline=True)
    embed.add_field(name='Gold:', value='<:gold:421856483706142741>' + ' ' + str(stats['goldEarned']), inline=True)
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
    embed=discord.Embed(title='**Summoner\'s Team Performance:**', description='<@' + userID + '>' + '\'s team\'s statistics during their last match', color=0x0ee796)
    embed.add_field(name='Kills', value=':crossed_swords:' + ' ' + str(totalTeamKills(match, teamID)), inline=True)
    embed.add_field(name='Deaths', value=':skull:' + ' ' + str(totalTeamDeaths(match, teamID)), inline=True)
    embed.add_field(name='Towers Killed', value=totalTeamTowerKills(match, teamID), inline=False)
    embed.add_field(name='Inhibitor Kills', value=totalTeamInhibitorKills(match, teamID), inline=True)
    embed.add_field(name='Dragons Killed', value=':dragon:' + ' ' + str(totalTeamDragonKills(match, teamID)), inline=True)
    embed.add_field(name='Barons Killed', value=totalTeamBaronKills(match, teamID), inline=True)
    embed.add_field(name='Rift Herald Kills', value=totalTeamRiftHeraldKills(match, teamID), inline=True)
    embed.add_field(name='Vilemaws Killed', value=totalTeamVilemawKills(match, teamID), inline=True)
    return embed


def getChampID(champ):
    champs = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + LoLkey).json()
    print(champs)
    for i in range(len(champs['data'])):
        if str(list(champs['data'].keys())[i]) == str(champ):
            print(champs['data'][list(champs['data'].keys())[i]]['id'])
            return champs['data'][list(champs['data'].keys())[i]]['id']
 
def getEmoji(champName):
    champName = str(champName).replace(" ", "")
    champName = str(champName).replace('\'', '')
    emojiID = 'oof'
    if ord(champName[0].lower()) >= ord('a') and ord(champName[0].lower()) <= ord('j'):
        for i in range(len(list(client.servers))):
            if list(client.servers)[i].id == '419162890503847937':
                for j in range(len(list(client.servers)[i].emojis)):
                    if list(client.servers)[i].emojis[j].name == champName:
                        emojiID = str(list(client.servers)[i].emojis[j].id)
                        return '<:'+ champName +':' + emojiID + '>'
    if ord(champName[0].lower()) >= ord('k') and ord(champName[0].lower()) <= ord('r'):
        for i in range(len(list(client.servers))):
            if list(client.servers)[i].id == '421470760637562890':
                for j in range(len(list(client.servers)[i].emojis)):
                    if list(client.servers)[i].emojis[j].name == champName:
                        emojiID = str(list(client.servers)[i].emojis[j].id)
                        return '<:'+ champName +':' + emojiID + '>'
    if ord(champName[0].lower()) >= ord('s') and ord(champName[0].lower()) <= ord('z'):
        for i in range(len(list(client.servers))):
            if list(client.servers)[i].id == '421471209612640271':
                for j in range(len(list(client.servers)[i].emojis)):
                    if list(client.servers)[i].emojis[j].name == champName:
                        emojiID = str(list(client.servers)[i].emojis[j].id)
                        return '<:'+ champName +':' + emojiID + '>'

        

def sendCustomIconEmoji(icon):
        for i in range(len(list(client.servers))):
            if list(client.servers)[i].id == '421471209612640271':
                for j in range(len(list(client.servers)[i].emojis)):
                    if list(client.servers)[i].emojis[j].name == icon:
                        emojiID = str(list(client.servers)[i].emojis[j].id)
                        return '<:'+ icon +':' + emojiID + '>'
                    
                    
def registerMessage(discordUser, userID):
    embed=discord.Embed(description='<@' + userID + '>' + ' Registered with League-Buddy as level ' + str(summoners[discordUser]['summonerLevel']) + ' summoner, in ' + summonerRegion[discordUser] + '.', color=0x0ee796)
    embed.set_author(name=summoners[discordUser]['name'],icon_url='http://ddragon.leagueoflegends.com/cdn/8.5.2/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
    return embed

def changeSummonerMessage(discordUser, userID):
    embed=discord.Embed(description='<@' + userID + '>' + ' League-Buddy summoner changed', color=0x0ee796)
    embed.set_author(name=summoners[discordUser]['name'],icon_url='http://ddragon.leagueoflegends.com/cdn/8.5.2/img/profileicon/' + str(summoners[discordUser]['profileIconId']) + '.png')
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

def getLastMatch(account_id, discordUser):
    match = requests.get('https://' + str(summonerRegion[discordUser].lower()) + base_url + 'match/v3/matches/' + str((requests.get('https://' + str(summonerRegion[discordUser].lower()) + base_url + 'match/v3/matchlists/by-account/'
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

def getChampName(champID, discordUser):
    message = requests.get('https://' + summonerRegion[discordUser] + base_url + 'static-data/v3/champions/' + champID + '?locale=en_US&api_key=' + LoLkey).json()
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

def getSummoner(summonerName, discordUser):
    summoner = requests.get('https://' + summonerRegion[discordUser] + base_url + 'summoner/v3/summoners/by-name/'+ summonerName + '?api_key=' + LoLkey).json()
    return summoner

def registerSummoner(summoner, discordID):
    if discordID not in summoners.keys():
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
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('lb! last match report'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, embed=lastMatchMessage(str(message.author), message.server, str(message.author.id), getLastMatch(str(summoners[str(message.author)]['accountId']), str(message.author))))
    if message.content.startswith('lb! last match report'):
        accountID = str(summoners[str(message.author)]['accountId'])
        match = getLastMatch(accountID, str(message.author))
        teamID = getTeam(match, summoners[str(message.author)]['accountId'])
        await client.send_message(message.channel, embed=lastMatchTeamMessage(match, teamID, message.author.id))
    if message.content.startswith('lb! register'):
        text = messageTokenizor(message.content)
        registerRegion(str(message.author), text[3].upper())
        registerSummoner(getSummoner(text[4], str(message.author)), str(message.author))
        await client.send_message(message.channel, embed=registerMessage(str(message.author), str(message.author.id)))
    if message.content.startswith('lb! summoner'):
        await client.send_message(message.channel, embed=summonerStats(str(message.author), str(message.author.id)))
    if message.content.startswith('lb! change summoner'):
        text = messageTokenizor(message.content)
        registerRegion(str(message.author), text[4].upper())
        changeSummoner(getSummoner(text[5], str(message.author)), str(message.author))
        await client.send_message(message.channel, embed=changeSummonerMessage(str(message.author), str(message.author.id)))
    if message.content.startswith('lb! emote'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, getEmoji(text[3]))
    if message.content.startswith('lb! oof'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, sendCustomIconEmoji(text[3]))
    if message.content.startswith('lb! champion'):
        text = messageTokenizor(message.content)
        await client.send_message(message.channel, embed=champMessage(text[3]))
#Discord Bot Authentication data
client.run(token)
