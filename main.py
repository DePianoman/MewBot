import discord, aiohttp, asyncio, sqlite3
from discord.ext.commands import Bot
from discord.ext import commands
from discord import *

bot_prefix = "mb!"
client = commands.Bot(command_prefix=bot_prefix)

client.remove_command('help')

@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))


@client.event
async def on_message(message):
    conn = sqlite3.connect('./Resources/Interactive/Prefixes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Prefixes")
    user_id = message.author.id
    buffer = c.fetchall()
    data = [i[0] for i in buffer]
    c.close()
    conn.close()
    if(user_id in data):
        cprefix = buffer[data.index(user_id)][-1]
        if(message.content.startswith(cprefix) and not message.author.bot):
            message.content = "mb!" + message.content[len(cprefix):].split()[0].lower() + ' ' + message.content[len(cprefix):].split()[1] if len(message.content[len(cprefix):].split()) != 1 else "mb!" + message.content[len(cprefix):].split()[0].lower()
            game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
            await client.change_presence(activity=game)
            payload = {"server_count": str(len(client.guilds))}
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post('https://botsfordiscord.com/api/bot/' + str(client.user.id), data=payload, headers={"Authorization": open('C:/TOKENS/BFD.txt').read()})
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("C:/TOKENS/DBL.txt").read()})
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data={"guilds": len(client.guilds), "users": x}, headers={"Authorization": open("C:/TOKENS/DBL2.txt").read()})
            await client.process_commands(message)
    else:
        if(message.content.startswith("mb!") and not message.author.bot):
            game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
            await client.change_presence(activity=game)
            payload = {"server_count": str(len(client.guilds))}
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post('https://botsfordiscord.com/api/bot/' + str(client.user.id), data=payload, headers={"Authorization": open('C:/TOKENS/BFD.txt').read()})
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("C:/TOKENS/DBL.txt").read()})
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data={"guilds": len(client.guilds), "users": x}, headers={"Authorization": open("C:/TOKENS/DBL2.txt").read()})
            await client.process_commands(message)

extensions = ["Resources.Modules.Fun", "Resources.Modules.Encryption", "Resources.Modules.Money", "Resources.Modules.Info", "Resources.Modules.Mod"]

for i in extensions:
    client.load_extension(i)
client.run(open("C:/TOKENS/TOKEN.txt").read())
