import discord
import nltk
import requests

base_url = 'https://na1.api.riotgames.com/lol/'
global summoners
summoners = {}
def getLastMatch(account_id):
    match = requests.get(base_url + 'match/v3/matches/' + str((requests.get(base_url + 'match/v3/matchlists/by-account/'
                        + account_id + '/recent?api_key=RGAPI-03794653-30ed-48c1-a60b-db4fed864aa9').json()['matches'][0]['gameId']))
                        + '/?api_key=RGAPI-03794653-30ed-48c1-a60b-db4fed864aa9').json()
    return match

def getSummoner(summonerName):
    summoner = requests.get(base_url + 'summoner/v3/summoners/by-name/'+ summonerName + '?api_key=RGAPI-03794653-30ed-48c1-a60b-db4fed864aa9').json()
    return summoner

def registerSummoner(summoner, discordID):
    if discordID not in summoners:
        summoners[discordID] = summoner 
    
    print(summoners)
def messageTokenizor(message):
    tokens = nltk.word_tokenize(message)
    return tokens
    
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
        print(summoners[str(message.author)]['accountId'])
        print(str(getLastMatch(str(summoners[str(message.author)]['accountId']))))
    if message.content.startswith('!register'):
        text = messageTokenizor(message.content)
        registerSummoner(getSummoner(text[2]), str(message.author))
        
#Discord Bot Authentication data
client.run('Mzk3Mjc1Njg3OTY4NTcxMzkz.DXZtDA.l_w70uLpD2Zkh8iNRGvImlTri1Q')
