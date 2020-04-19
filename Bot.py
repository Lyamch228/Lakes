import discord
import os
from discord.ext  import commands
import random
import nekos
import logging
import yaml
import sqlite3
import time
import random
import re

bot = commands.Bot(command_prefix = "+")
bot.remove_command("help")

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
@commands.has_permissions(administrator = True)
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
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= " PornHub | +help"))

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 1/2.')
    embed.add_field(name="mute", value="мутить нарушителей", inline=False)
    embed.add_field(name="unmute", value="размутить нарушителя", inline=False)
    embed.add_field(name="tempmute", value="замутить участника сервера на время", inline=False)
    embed.add_field(name="ban", value="забанить нарушителя", inline=False)
    embed.add_field(name="kick", value="кикнуть нарушителя", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def help2(ctx):
    embed = discord.Embed(title="commands", description="", color=0xeee657)
    embed.set_footer(text='help command 2/2.')
    embed.add_field(name="шар", value="гадание", inline=False)
    embed.add_field(name="avatar", value="показывает аватар участника", inline=False)
    embed.add_field(name="teleportation", value="телепортировать участника с 1 голосовго канала на вторую", inline=False)
    embed.add_field(name="gay", value="показывает на сколько вы гей", inline=False)
    embed.add_field(name="serverinfo", value="узнать информацию о сервере", inline=False)
    await ctx.send(embed=embed)
    
@bot.command(pass_context=True, aliases=["whois", "info" ])
 
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]



    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f'User Info -{member}')
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)


    embed.add_field(name='ID:', value=member.id)
    embed.add_field(name='Guild name:', value=member.display_name)

    embed.add_field(name='Created at:', value=member.created_at.strftime('%a, %#d %B %Y %I:%M %p EST'))
    embed.add_field(name='Joined at:', value=member.joined_at.strftime('%a, %#d %B %Y %I:%M %p EST'))

    embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))

    embed.add_field(name='Top role:', value=member.top_role.mention)
    
    embed.add_field(name='bot?', value=member.bot) 

    await ctx.send(embed=embed)

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
async def gay(ctx):
    random.randint(1, 100)
    embed = discord.Embed(title = None, description=f"{ctx.author} is {random.randint(1, 100)}% gay.")
    await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, member : discord.Member):
    await ctx.message.delete()
    emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('kiss'))
    await ctx.send(embed=emb)

@bot.command()
async def hug(ctx, member : discord.Member):
    await ctx.message.delete()
    emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('hug'))
    await ctx.send(embed=emb)

@bot.command()
async def slap(ctx, member : discord.Member):
    await ctx.message.delete()
    emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('spal'))
    await ctx.send(embed=emb)

@bot.command()
async def pat(ctx, member : discord.Member):
    await ctx.message.delete()
    emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.')
    emb.set_image(url=nekos.img('pat'))
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
async def rank(ctx):
    
    try:
        _, member = (ctx.message.content).split(' ', 1)
        member = re.sub("[^0-9]", "", member)
    except:
        member = ctx.message.author.id
    
    db = sqlite3.connect('data/users.db')
    c = db.cursor()

    c.execute('SELECT user.*, (SELECT count(*) FROM users AS members WHERE members.rawexp > user.rawexp) as Rank FROM users AS user WHERE id = ?',
              (ctx.message.author.id, ))
    
    user = c.fetchone()
    db.close()

    rank = str(user[6] + 1)

    embed = discord.Embed(title='{}\'s Information'.format(ctx.message.author.name)) \
            .set_thumbnail(url=ctx.message.author.avatar_url) \
            .add_field(name='Rank', value='#' + rank) \
            .add_field(name='Level', value=user[2]) \
            .add_field(name='EXP', value='{}/{}'.format(user[3], threshold(user[2]))) \
            .add_field(name='Raw EXP', value=user[4]) \

    await bot.say(embed=embed)

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.content.startswith('l>'):
        await bot.process_commands(message)
        return
        
    db = sqlite3.connect('data/users.db')
    c = db.cursor()

    c.execute('SELECT * FROM users WHERE id= ?', (message.author.id,))
    user = c.fetchone()
        
    if user is None:
        await bot.send_message(message.channel, 'Looks like you\'re new! Welcome to level 1. Initializing player...')
        c.execute('INSERT INTO users(id, name, level, exp, rawexp, time) VALUES(?,?,?,?,?,?)', (message.author.id, message.author.name, 1, 0, 0, time.time()))
        db.commit()
        db.close()
        return

    if message.author.name != user[1]:
        c.execute('UPDATE users SET name = ? WHERE id= ?', (message.author.name, message.author.id))

    if (time.time() - user[5]) > 60:
        addedexp = random.randint(10, 25)
        exp = user[3] + addedexp
        rawexp = user[4] + addedexp
        c.execute('UPDATE users SET exp = ?, rawexp = ?, name = ?, time = ? WHERE id= ?', (exp, rawexp, message.author.name, time.time(), message.author.id))

        if (exp > threshold(user[2])):
            level = user[2] + 1
            c.execute('UPDATE users SET exp = ?, level = ? WHERE id= ?', (0, level, message.author.id))
            await bot.send_message(message.channel, 'Wowza! You leveled up! Your level is now **{}**.'.format(level))

    db.commit()
    db.close()

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("LevelBot Mee6Clone")
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name='a meme', url="https://twitch.tv/meme", type=1))

    #Initialize database.
    db = sqlite3.connect('data/users.db')
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, level INT, exp INTEGER, rawexp INTEGER, time REAL)')
    db.commit()

	
bot.run(os.getenv('TOKEN'))
