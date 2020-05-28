import discord
import os
import asyncio
import json
import sqlite3
from discord.ext  import commands
import random
import nekos
from discord.utils import get
import youtube_dl

def get_prefix(bot, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	return prefixes[str(message.guild.id)]
	
bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command("help")

@bot.event
async def on_guild_join(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	prefixes[str(guild.id)] = 'la'
	
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)
		
		
@bot.event
async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	prefixes.pop(str(guild.id))
	
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)

	
@bot.command()
async def setprefix(ctx, prefix):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	prefixes[str(ctx.guild.id)] = prefix
	
	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)
	await ctx.send(f"префикс на этом сервер: {prefix}")

@bot.command()
async  def load(ctx, extension):
	bot.initial_extension(f'{extension}')
    
@bot.command()
async def reload(ctx, *, msg):
    """Load a module."""
    await ctx.message.delete()
    try:
        if os.path.exists("custom_cogs/{}.py".format(msg)):
            bot.reload_extension("custom_cogs.{}".format(msg))
        elif os.path.exists("cogs/{}.py".format(msg)):
            bot.reload_extension("cogs.{}".format(msg))
        else:
            raise ImportError("No module named '{}'".format(msg))
    except Exception as e:
        await ctx.send('Failed to reload module: `{}.py`'.format(msg))
        await ctx.send('{}: {}'.format(type(e).__name__, e))
    else:
        await ctx.send('Reloaded module: `{}.py`'.format(msg)) 
        
for filename in os.listdir("./cogs"):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready(*args):
    type = discord.ActivityType.listening
    guilds = await bot.fetch_guilds(limit=None).flatten()
    activity = discord.Activity(name = f"+rank", type = type)
    status = discord.Status.online
    await bot.change_presence(activity = activity, status = status)
    print("Бот готов к работе.")

conn = sqlite3.connect("LolBot.db")  # подключаем таблицу
cursor = conn.cursor()  # управление таблицей

@bot.event
async def on_message(message):
    cursor.execute(f"SELECT id FROM users WHERE id={ctx.author.id}")
    if cursor.fetchone() == None:  # Если игрока нету в БД, но он на сервере, то..
        cursor.execute(f"INSERT INTO users VALUES ({message.author.id}, '{message.author.name}', '<@{message.author.id}>', 1, 0)")  # вводим данные игрока согласно созданной таблице
        print(f'Я закинул в бд пользователя {message.author.name}.')
    else:
        pass
    if len(message.content) >= 3:  # Если сообщение больше 3 букв
        # беру всю инфу из id пользевателя
        for row in cursor.execute(f"SELECT lvl,xp FROM users_{message.guild.id} WHERE id={message.author.id}"):
            # перевожу все в переменные
            LVL = row[0]
            XP = row[1]
            XP += randint(1, 20)  # Делаю + 1 до 5 рандомно
            if XP >= 100:  # Если XP == 30 то обновляю LVL
                LVL += 1
                XP = 0

            cursor.execute(f"UPDATE users SET lvl = {LVL}, xp = {XP} WHERE id={message.author.id}")
            conn.commit()
    await bot.process_commands(message)

@bot.command()
async def rank(ctx, member: discord.Member = None):
    if member == None or not member:
        member = ctx.author
    for row in cursor.execute(f"SELECT lvl,xp FROM users WHERE id={member.id}"):
        LVL = row[0]
        XP = row[1]
        emb = discord.Embed(title='Ранг', description=f'Ранг пользователя {member.name}')
        emb.add_field(name='Уровень', value=f'Уровень пользователя {member.name} - {LVL}')
        emb.add_field(name='XP', value=f'XP у пользователя {member.name} - {XP}')


@bot.command(pass_context=True, aliases=["telep", "tp" ])
async def teleportation(ctx, arg=None, member: discord.Member = None):
        channels = ctx.author.voice.channel.id
        await ctx.message.delete()
        if not channels:
            await ctx.send('Нужно находиться в войсе', delete_after=10)
            return
        if not arg:
            await ctx.send('Нужно указать, куда переместить юзеров', delete_after=10)
            return
        voice = ctx.guild.voice_channels
        print(voice)
        try:
            vchannel = voice[int(arg) - 1]
        except:
            await ctx.send('Неправильный аргумент', delete_after=10)
            return
        if member == None:
            x = ctx.author.voice.channel.members
            for mem in x:
                    await mem.edit(voice_channel=vchannel)
        else:
            await member.edit(voice_channel=vchannel)
				
@bot.command()
async def ping(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    emb = discord.Embed(
        title= 'Текущий пинг',
        description= f'{bot.ws.latency * 1000:.0f} ms'
    )
    await ctx.send(embed=emb)

@bot.command()
@commands.has_permissions(ban_members = True)
async def echo(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command()
async def suggest( ctx , * , agr ):
    suggest_chanell = bot.get_channel( 707625071426011276 ) #Айди канала предложки
    embed = discord.Embed(title=f"{ctx.author.name} Предложил :", description= f" {agr} \n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)

    message = await suggest_chanell.send(embed=embed)
    await message.add_reaction(':white_check_mark:')
    await message.add_reaction(':negative_squared_cross_mark:')

@bot.command()
@commands.has_permissions(ban_members=True)
async def say(ctx, channel: discord.TextChannel, *, text):
    attachments = ctx.message.attachments
    emb = discord.Embed(
        description = text,
        colour = 0x00ff80
    )
    for a in attachments:
        if a.url != None:
            emb.set_image(url= f"{a.url}")    
    await channel.send(embed=emb)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= " Test | lahelp"))

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 1/4.')
    embed.add_field(name="mute", value="мутить участника", inline=True)
    embed.add_field(name="tempmute", value="мут участника на время", inline=True)
    embed.add_field(name="ban", value="бан участника", inline=True)
    embed.add_field(name="kick", value="кик участника", inline=True)
    embed.add_field(name="unmute", value="размут участника", inline=True)
    await ctx.send(embed=embed)



@bot.command(aliases=["help 2"])
async def help2(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 2/4.')
    embed.add_field(name="шар", value="гадание", inline=True)
    embed.add_field(name="avatar", value="показывает аватар участника", inline=True)
    embed.add_field(name="teleportation", value="телепортировать участника с 1 голосовго канала на вторую", inline=True)
    embed.add_field(name="gay", value="показывает на сколько вы гей", inline=True)
    embed.add_field(name="suggest", value="предложить идею,для улучшения серверв", inline=True)
    embed.add_field(name="serverinfo", value="узнать информацию о сервере", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=["help 3"])
async def help3(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 3/4.')
    embed.add_field(name="kiss", value="поцеловать участника сервера", inline=True)
    embed.add_field(name="hug", value="обнять участника сервера", inline=True)
    embed.add_field(name="slap", value="ударить участника сервера", inline=True)
    embed.add_field(name="pat", value="погладить участника сервера", inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=["help 4"])
async def help4(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 4/4.')
    embed.add_field(name="setprefix", value="изменить префикс бота", inline=True)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions( ban_members=True )
async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 707612817204838491) #Айди роли
    channel_log = bot.get_channel(704191405807108186) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( mute_role )   

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))
 

@bot.command(aliases =['8ball'])
async def шар(ctx, *, question):
	await ctx.send(random.choice(["конечно",
	           "да",
	           "предврешено!",
	            "нет",
	             "конечно, нет",
	             "соглашусь",
	             "Хорошие перспективы :ok_hand:",
	             "мой ответ, нет :no_entry_sign:",
	             "нет, и никогда."]))
	             
@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.guild.name), description="Информация о сервере.", color=0x000000)
    embed.set_footer(text= f'Вызвано: {ctx.message.author}')
    embed.add_field(name="Name", value=ctx.guild.name, inline=True)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="роли", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="участники", value=len(ctx.guild.members))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)	             


@bot.command(name='cl')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.command()
async def gay(ctx):
    random.randint(1, 100)
    embed = discord.Embed(title = None, description=f"{ctx.author} is {random.randint(1, 100)}% gay.")
    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, member : discord.Member):
    emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('kiss'))
    await ctx.send(embed=emb)

@bot.command()
async def hug(ctx, member : discord.Member):
    emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('hug'))
    await ctx.send(embed=emb)

@bot.command()
async def slap(ctx, member : discord.Member):
    emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('spal'))
    await ctx.send(embed=emb)

@bot.command()
async def pat(ctx, member : discord.Member):
    emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('pat'))
    await ctx.send(embed=emb)

@bot.command()
async def bite(ctx, member : discord.Member):
    emb = discord.Embed(description= f'{member.mention}, Вас укусил(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('bite'))
    await ctx.send(embed=emb)

	
@slap.error
async def slap_error(ctx, error):
	 if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("+slap [ping]")
          
@hug.error
async def hug_error(ctx, error):
	 if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("+hug [ping]")

@kiss.error
async def kiss_error(ctx, error):
	 if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("+kiss [ping]")

@pat.error
async def pat_error(ctx, error):
	 if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("+pat [ping]")

@bot.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, amount: int):
            await ctx.channel.purge(limit=amount)
            await ctx.send("ваши сообщении удалились")

@bot.command(pass_context=True)
@commands.has_permissions(administrator = True)
async def addrole(ctx, member : discord.Member, *, role : discord.Role):
    await member.add_roles(role)
    await ctx.send(f"added the role '{role}' to {member}!") 
  
@bot.command(pass_context=True)
@commands.has_permissions(administrator = True)
async def removerole(ctx, member : discord.Member, *, role : discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"removed the role '{role}' to {member}!") 

@bot.command(pass_context=True, aliases=["whois", "info" ])
 
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]



    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f'User Info -{member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)


    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='ник на сервере :', value=member.display_name)

    embed.add_field(name='создал аккаунт:', value=member.created_at.strftime('%a, %#d %B %Y %I:%M %p EST'))
    embed.add_field(name='присоединился в', value=member.joined_at.strftime('%a, %#d %B %Y %I:%M %p EST'))

    embed.add_field(name=f'Роли: ({len(roles)})', value=' '.join([role.mention for role in roles]))

    embed.add_field(name='самая большая роль:', value=member.top_role.mention)
    
    embed.add_field(name='Бот?', value=member.bot) 

    await ctx.send(embed=embed)    

@bot.command()                 
async def avatar(ctx, member : discord.Member = None):
                            user = ctx.message.author if (member == None) else member
                            await ctx.message.delete()
                            embed = discord.Embed(title=f'Аватар пользователя {user}', description= f'[Ссылка на изображение]({user.avatar_url})', color=user.color)
                            embed.set_footer(text= f'Вызвано: {ctx.message.author}', icon_url= str(ctx.message.author.avatar_url))
                            embed.set_image(url=user.avatar_url)
                            await ctx.send(embed=embed)
			
@bot.command()
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		engine = pyttsx3.init()
		engine.say('Привет, человечушки. Как жизнь на земле!?')
		engine.runAndWait()

@bot.command()
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(bot.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.connect()

@bot.command()
async def play(ctx, url : str):
	song_there = os.path.isfile('song.mp3')

	try:
		if song_there:
			os.remove('song.mp3')
			print('[log] Старый файл удален')
	except PermissionError:
		print('[log] Не удалось удалить файл')

	await ctx.send('Пожалуйста ожидайте')

	voice = get(bot.voice_clients, guild = ctx.guild)

	ydl_opts = {
		'format' : 'bestaudio/best',
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print('[log] Загружаю музыку...')
		ydl.download([url])

	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			name = file
			print(f'[log] Переименовываю файл: {file}')
			os.rename(file, 'song.mp3')

	voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	song_name = name.rsplit('-', 2)
	await ctx.send(f'Сейчас проигрывает музыка: {song_name[0]}')


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id: # Проверка бот ли это
        if message.guild: # Проверка на сервере ли это
            await bot.process_commands(message) # Выполнение команды
        else: 
            await message.author.send("Не-а, я не хочу чтобы ты меня задудосил ошибками в консоли от того что некоторые команды не приспособны к личке.")

bot.run(os.getenv('TOKEN'))
