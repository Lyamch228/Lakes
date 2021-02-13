import discord
import os
import asyncio
import json
from discord.ext  import commands
import random
from Cybernator import Paginator as pag
import nekos
from discord.utils import get
import youtube_dl
import wikipedia

bot = commands.Bot(command_prefix = "la")
bot.remove_command("help")
bot.load_extension("jishaku")

@bot.command()
async  def load(ctx, extension):
	bot.initial_extension(f'{extension}')
    
@bot.command()
async def setprefix(ctx, prefix):
     bot.command_prefix = prefix
     await ctx.send(f"Префикс изменен на ``{prefix}``")
	
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
    suggest_chanell = bot.get_channel( 731928849968791616) #Айди канала предложки
    embed = discord.Embed(title=f"{ctx.author.name} Предложил :", description= f" {agr} \n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)

    message = await suggest_chanell.send(embed=embed)
    await message.add_reaction('✔')
    await message.add_reaction('✖')
    await ctx.message.delete()

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
	embed1 = discord.Embed(title = 'Игры 🔫')
	embed1.add_field(name=f'lasaper', value='Команда для игры --"сапёр"')
	embed1.add_field(name=f'laknb', value='Команда для игры --"камень, ножницы, бумага"')
	embed1.add_field(name=f'laшар', value='Команда для игры --"шар"')
	embed2 = discord.Embed(title = 'Модерация 📚')
	embed2.add_field(name=f'lamute', value='lamute <участник> (время) <причина>')
	embed2.add_field(name=f'laban', value='laban <участник> (время) <причина>')
	embed2.add_field(name=f'lakick', value='lakick <участник> <причина>')
	embed2.add_field(name=f'launmute', value='launmute <участник>')
	embed3 = discord.Embed(title = 'Информация 📙')
	embed3.add_field(name=f'laserverinfo', value='Информация о сервере')
	embed3.add_field(name=f'lauserinfo', value='Информация о Участнике')
	embed3.add_field(name=f'laavatar', value='аватар участника')
	embed3.add_field(name=f'lasuggest', value='идеи для сервера')
	embed4 = discord.Embed(title = 'Фан 📘')
	embed4.add_field(name=f'lakiss', value='поцеловать участника')
	embed4.add_field(name=f'lahug', value='обнять участника')
	embed4.add_field(name=f'laslap', value='шлепнуть участника')
	embed4.add_field(name=f'lateleportation', value='телепортировать участника с одного голосового канала на другой')
	embeds = [embed1, embed2, embed3, embed4]
	message = await ctx.send(embed=embed1)
	page = pag(bot, message, only=ctx.author, use_more=False, embeds=embeds)
	await page.start()

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

@bot.command()
@commands.is_owner()
async def lelave(ctx):
    await ctx.message.delete()
    await ctx.guild.leave()

@bot.command(name='cl')
@commands.has_permissions(ban_members=True)
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

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
    emb.set_image(url=nekos.img('slap'))
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

@bot.command()
async def hentai(ctx, member : discord.Member):
    emb.set_image(url=nekos.img('hentai'))
    await ctx.send(embed=emb))

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


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id: # Проверка бот ли это
        if message.guild: # Проверка на сервере ли это
            await bot.process_commands(message) # Выполнение команды
        else: 
            await message.author.send("Не-а, я не хочу чтобы ты меня задудосил ошибками в консоли от того что некоторые команды не приспособны к личке.")

@bot.command()
async def wiki(ctx, *, args):
  try:
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(f'{args}')
    summ = wikipedia.summary(f'{args}', sentences=5)
    emb = discord.Embed(title=new_page.title,
                        description=f"{summ}",
                        color=0xc582ff)
    emb.add_field(name="Для полного ознакомления со статьей, перейдите по ссылке:", value=f"[M]({new_page.url})")
    await ctx.send(embed=emb)
  except Exception:
    return await ctx.send('Неоднозначный аргумент, уточните статью', delete_after=10)
    await ctx.send(embed = emb)

@bot.command()
async def knb(ctx, move: str = None):
    solutions = ["`ножницы`", "`камень`", "`бумага`"]
    winner = "**НИЧЬЯ**"
    p1 = solutions.index(f"`{move.lower()}`")
    p2 = randint(0, 2)
    if p1 == 0 and p2 == 1 or p1 == 1 and p2 == 2 or p1 == 2 and p2 == 0:
        winner = f"{ctx.message.author.mention} ты **Проиграл**"
    elif p1 == 1 and p2 == 0 or p1 == 2 and p2 == 1 or p1 == 0 and p2 == 2:
        winner = f"{ctx.message.author.mention} ты **Выиграл**"
    emb = discord.Embed(title = 'Камень ножницы бумага', description = f"{ctx.message.author.mention} **=>** {solutions[p1]}\n" + f"{ctx.message.author.mention} **=>** {solutions[p1]}\n" + f"{winner}")
    await ctx.send(embed = emb)

@bot.command()
async def saper(ctx):
    embed = discord.Embed(description='''
                     Держи :smile:
||0️⃣||||0️⃣||||0️⃣||||1️⃣||||1️⃣||||2️⃣||||1️⃣||||2️⃣||||1️⃣||||1️⃣||||
2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||2️⃣||||💥||||3️⃣||||💥||||1️⃣||||
💥||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||3️⃣||||💥||||2️⃣||||1️⃣||||
2️⃣||||2️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||2️⃣||||1️⃣||||1️⃣||||0️⃣||||
0️⃣||||0️⃣||||0️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||0️⃣||||0️⃣||||0️⃣||||
1️⃣||||1️⃣||||0️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||
💥||||1️⃣||||1️⃣||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||💥||||💥||||1️⃣||||
1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||||1️⃣||||2️⃣||||3️⃣||||2️⃣||||1️⃣||||
1️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||2️⃣||||💥||||1️⃣||||0️⃣||||0️⃣||||
💥||||2️⃣||||💥||||1️⃣||||1️⃣||||💥||||2️⃣||||2️⃣||||1️⃣||||1️⃣||||
1️⃣||||2️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||1️⃣||||💥||||1️⃣||
    ''', color=discord.Colour.orange())
    await ctx.send(embed=embed)



@bot.command()
@commands.has_permissions(view_audit_log = True)
async def unmute(ctx, member: discord.Member):
	muterole = discord.utils.get(ctx.guild.roles, id = 707612817204838491)
	emb = discord.Embed(title='АнМут', color=0xff0000)
	emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)
	emb.add_field(name='Нарушитель',value=member.mention,inline=False)
	await member.send(embed = emb)

@bot.command()
@commands.has_permissions(view_audit_log = True)
async def kick(ctx, member: discord.Member):
	emb = discord.Embed(title='Кик', color=0xff0000)
	emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)
	emb.add_field(name='Причина',value=reason,inline=False)
	emb.add_field(name='Время',value=time,inline=False)
	emb.add_field(name='Нарушитель',value=member.mention,inline=False)
	await member.kick()
	await member.send(embed = emb)

@bot.command()
@commands.has_permissions(view_audit_log = True)
async def ban(ctx, member: discord.Member, time:int, reason):
	emb = discord.Embed(title='ban', color=0xff0000)
	emb.add_field(name='Модератор',value=ctx.message.author.mention,inline=False)
	emb.add_field(name='Причина',value=reason,inline=False)
	emb.add_field(name='Время',value=time,inline=False)
	emb.add_field(name='Нарушитель',value=member.mention,inline=False)
	if member != None:
	               if member == ctx.message.author:
	               	await ctx.send('Вы не можете банить себя')
	await member.send(embed = emb)
	await member.ban()
	await asyncio.sleep(time)
	await member.unban()
	

bot.run(os.getenv('TOKEN'))
