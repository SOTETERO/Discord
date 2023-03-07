import discord
from gtts import gTTS
import os

token = os.environ("token")

class MyClient(discord.Client):
    
    def TTSPlay(self):
        if self.voice.is_playing():
            return
        
        if len(self.ttsStack) == 0:
            return
        
        ttsText = self.ttsStack[0]
        self.ttsStack = self.ttsStack[1:]
        
        try:
            tts = gTTS(text=ttsText, lang=self.voiceLanguage, slow=False)
            tts.save("tts.mp3")
        except:
            self.TTSPlay()
            
        self.voice.play(source=discord.FFmpegOpusAudio("tts.mp3"), after=lambda e : self.TTSPlay())
    
    async def on_ready(self):
        print("비숑준비")
        self.voice = None
        self.voiceChannel = None
        self.voiceLanguage = "ko"
        self.ttsStack = []
        
    async def on_message(self, message):
        if message.content == "":
            return
        
        print(message.content)
        content = message.content.split()
        if content[0] == "비숑이리온":  
            if message.author.voice == None: #음성 채널에 없을 경우
                pass
            elif self.voiceChannel == message.author.voice: #같은 음성 채널에 있는 경ㅇ 
                pass
            else:
                self.voice = await message.author.voice.channel.connect()
                self.voiceChannel = message.author.voice
                
                embed = discord.Embed(title="음성 채널 입장", description=f"- {self.voice.channel} - 입장", color=discord.Color.from_rgb(0, 0, 0))
                await message.channel.send(embed=embed)
                
        elif content[0] == "비숑언어":
            self.voiceLanguage = content[1]
            
            embed = discord.Embed(title="언어 변경", description=f"언어  -{self.voiceLanguage}- 변경", color=discord.Color.from_rgb(0, 0, 0))
            await message.channel.send(embed=embed)
        elif content[0] == "비숑도움말":
            
            embed = discord.Embed(title="비숑도움말", color=discord.Color.from_rgb(0, 0, 0))
            embed.add_field(name="비숑이리온", value="비숑이 음성 채널에 들어옵니다.", inline=False)
            embed.add_field(name="비숑언어 [언어]", value="비숑이 tts 언어를 설정합니다.", inline=False)
            
            await message.channel.send(embed=embed)
            
        else:
            if self.voiceChannel == message.author.voice:
                self.ttsStack.append(message.content)
                self.TTSPlay()
            
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)