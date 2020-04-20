import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
import asyncio

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	queues = {}

	@commands.command(pass_context=True, aliases=['j', 'joi'])
	async def join(self, ctx):
	    global voice
	    channel = ctx.message.author.voice.channel
	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_connected():
	        await voice.move_to(channel)
	    else:
	        voice = await channel.connect()

	    await voice.disconnect()

	    if voice and voice.is_connected():
	        await voice.move_to(channel)
	    else:
	        voice = await channel.connect()

	    await ctx.send(f"Подключение к каналу *{channel}*")


	@commands.command(pass_context=True, aliases=['l', 'lea'])
	async def leave(self, ctx):
	    channel = ctx.message.author.voice.channel
	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_connected():
	        await voice.disconnect()
	        await ctx.send(f"Отключение от канала *{channel}*")
	    else:
	        await ctx.send("Я не подключён ни к одному каналу")


	@commands.command(pass_context=True, aliases=['p', 'pla'])
	async def play(self, ctx, url: str):

	    def check_queue():
	        Queue_infile = os.path.isdir("./Queue")
	        if Queue_infile is True:
	            DIR = os.path.abspath(os.path.realpath("Queue"))
	            length = len(os.listdir(DIR))
	            still_q = length - 1
	            try:
	                first_file = os.listdir(DIR)[0]
	            except:
	                queues.clear()
	                return
	            main_location = os.path.dirname(os.path.realpath(__file__))
	            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
	            if length != 0:
	                song_there = os.path.isfile("song.mp3")
	                if song_there:
	                    os.remove("song.mp3")
	                shutil.move(song_path, main_location)
	                for file in os.listdir("./"):
	                    if file.endswith(".mp3"):
	                        os.rename(file, 'song.mp3')

	                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
	                voice.source = discord.PCMVolumeTransformer(voice.source)
	                voice.source.volume = 0.07

	            else:
	                queues.clear()
	                return

	        else:
	            queues.clear()



	    song_there = os.path.isfile("song.mp3")
	    try:
	        if song_there:
	            os.remove("song.mp3")
	            queues.clear()
	    except PermissionError:
	        await ctx.send("ERROR: Music playing")
	        return


	    Queue_infile = os.path.isdir("./Queue")
	    try:
	        Queue_folder = "./Queue"
	        if Queue_infile is True:
	            shutil.rmtree(Queue_folder)
	    except:
	        print("No old Queue folder")

	    await ctx.send("Пожалуйста, подождите")

	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    ydl_opts = {
	        'format': 'bestaudio/best',
	        'quiet': True,
	        'postprocessors': [{
	            'key': 'FFmpegExtractAudio',
	            'preferredcodec': 'mp3',
	            'preferredquality': '192',
	        }],
	    }

	    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	        ydl.download([url])

	    for file in os.listdir("./"):
	        if file.endswith(".mp3"):
	            name = file
	            os.rename(file, "song.mp3")

	    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
	    voice.source = discord.PCMVolumeTransformer(voice.source)
	    voice.source.volume = 0.07

	    nname = name.rsplit("-", 2)
	    await ctx.send(f"Играет: *{nname[0]}*")


	@commands.command(pass_context=True, aliases=['pa', 'pau'])
	async def pause(self, ctx):

	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_playing():
	        voice.pause()
	        await ctx.send("Музыка приостановлена")
	    else:
	        await ctx.send("Музыка не может быть приостановлена")


	@commands.command(pass_context=True, aliases=['r', 'res'])
	async def resume(self, ctx):

	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    if voice and voice.is_paused():
	        voice.resume()
	        await ctx.send("Музыка возобновлена")
	    else:
	        await ctx.send("Музыка не может быть возобновлена")


	@commands.command(pass_context=True, aliases=['s', 'sto'])
	async def stop(self, ctx):
	    voice = get(self.bot.voice_clients, guild=ctx.guild)

	    queues.clear()

	    if voice and voice.is_playing():
	        voice.stop()
	        await ctx.send("Музыка остановлена")
	    else:
	        await ctx.send("Музыка не может быть остановлена")


	@commands.command(pass_context=True, aliases=['q', 'que'])
	async def queue(self, ctx, url: str):
	    Queue_infile = os.path.isdir("./Queue")
	    if Queue_infile is False:
	        os.mkdir("Queue")
	    DIR = os.path.abspath(os.path.realpath("Queue"))
	    q_num = len(os.listdir(DIR))
	    q_num += 1
	    add_queue = True
	    while add_queue:
	        if q_num in queues:
	            q_num += 1
	        else:
	            add_queue = False
	            queues[q_num] = q_num

	    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

	    ydl_opts = {
	        'format': 'bestaudio/best',
	        'quiet': True,
	        'outtmpl': queue_path,
	        'postprocessors': [{
	            'key': 'FFmpegExtractAudio',
	            'preferredcodec': 'mp3',
	            'preferredquality': '192',
	        }],
	    }

	    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	        ydl.download([url])
	    await ctx.send("Добавлена песня " + str(q_num) + " в плейлист")

	@commands.command(pass_context=True, aliases=['n', 'nex'])
	async def next(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		if voice and voice.is_playing():
			voice.stop()
			await ctx.send("Следующая песня...")
		else:
			await ctx.send("В данный момент музыка не воспроизводится.")


	

def setup(bot):
	bot.add_cog(Music(bot))