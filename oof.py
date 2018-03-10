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
champEmojis = {}



def wowie(server):
    response = requests.get('http://placehold.it/120x120&text=image1')
    img = Image.open(BytesIO(response.content))
    print(img)
    emote = client.create_custom_emoji(server=server, name='testEmote', image=img)
    #client.create_custom_emoji(server=server, name='testEmote', image=img)
    print(emote)
    print(server.emojis)
    champEmojis['testEmote'] = server.emojis
    emojiID = 'oof'
    for i in range(len(server.emojis)):
        if server.emojis[i].name == 'testEmote':
            emojiID = str(server.emojis[i].id)
    return '<:testEmote:' + emojiID + '>'







def iterChamps():
    #champIds = requests.get(base_url + 'platform/v3/champions?api_key=' + LoLkey).json()['champions']
    champs = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&api_key=RGAPI-4bc41e73-5b73-4591-b975-d37d4d0c484f').json()['data']
    print(champs)
    for i in range(len(champs)):
        champName = champs[list(champs.keys())[i]]['key']
        print(champName)
        response = requests.get('http://ddragon.leagueoflegends.com/cdn/8.5.2/img/champion/'
                                + str(champName).replace(" ", "") + '.png')
        img = Image.open(BytesIO(response.content))
        img.save(str(champName) + '.png')














        
def champEmoji(server, userChamp):
    if userChamp not in champEmojis.keys():
        return makeChampionEmoji(server, userChamp)
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>' 

def makeChampionEmoji(server, userChamp):
    response = requests.get('http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + str(userChamp) + '.png')
    img = Image.open(BytesIO(response.content))
    print(response)
    print(img)
    client.create_custom_emoji(server=server, name=userChamp, image=img)
    print(server.emojis)
    champEmojis[userChamp] = server.emojis
    return '<:'+ str(userChamp) + ':' + str(champEmojis[userChamp]) + ':>'

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
