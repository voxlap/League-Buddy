import discord
import nltk
import requests
import time
from PIL import Image
from io import BytesIO


base_url = 'https://na1.api.riotgames.com/lol/'
validRegions = ['NA1', 'RU', 'KR', 'PBE1', 'BR1', 'OC1', 'JP1', 'EUN1', 'EUW1', 'TR1', 'LA1', 'LA2']
with open('Lolkey.txt', 'r+') as myfile:
    LoLkey = str(myfile.read())
client = discord.Client()
with open('discordToken.txt', 'r+') as myfile:
    token = str(myfile.read())

def iterChamps():
    #champIds = requests.get(base_url + 'platform/v3/champions?api_key=' + LoLkey).json()['champions']
    champs = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + LoLkey).json()['data']
    print(champs)
    for i in range(len(champs)):
        champ = champs[list(champs.keys())[i]]['key']
        time.sleep(140)
        print(champ)
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
        with open('champMessages\\' + champ + 'champMessage.txt', 'w+') as myFile:
            myFile.seek(0, 2)
            myFile.write(str(embed.to_dict()))
    return

def getChampID(champ):
    champs = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=' + LoLkey).json()
    for i in range(len(champs['data'])):
        if str(list(champs['data'].keys())[i]) == str(champ):
            return champs['data'][list(champs['data'].keys())[i]]['id']
 
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


@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=' around, ig'))
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('lb! make emotes'):
        print(message.server.id)
        iterChamps()
#Discord Bot Authentication data
client.run(token)
