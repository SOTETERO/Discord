import discord
import gtts

class MyClient(discord.Client):
    
    async def on_ready(self):
        print("봇준비")

    async def on_message(self, message):
        print(message.content)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTA2MTkzODc2NzQ1MzIyNTAwMA.GDAxk-.L3pIiPhfVrpYkVSkrTrTrmgd_65Qk791igW-Ys')