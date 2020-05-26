import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '+')

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

bot.run('''Njk5NjIyOTEzODIwODUyNjI2.Xsz4hQ.ITurDEGcZLu5bMbDs4e-nxg-I80''')