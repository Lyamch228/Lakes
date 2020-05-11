import discord
from discord.ext import commands
from random import choice

class giveaway(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
    
    @commands.command()
    async def gstart(self, ctx, seconds: int, *, text):
        '''простая команда создания розыгрыша-раздачи
        Время писать по схеме:   секунды, далее, произвольный текст приза'''
        def time_end_form(seconds):
            h = seconds // 3600
            m = (seconds - h * 3600) // 60
            s = seconds % 60
            if h < 10:
                h = f"0{h}"
            if m < 10:
                m = f"0{m}"
            if s < 10:
                s = f"0{s}"
            time_reward = f"{h} : {m} : {s}"
            return time_reward
        author = ctx.message.author
        time_end = time_end_form(seconds)
        message = await ctx.send(f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}")
        await message.add_reaction("🎲")
        while seconds > -1:
            time_end = time_end_form(seconds)
            text_message = f"Розыгрыш!\nРазыгрывается:{text}\nЗавершится через {time_end}"
            await message.edit(content=text_message)
            await asyncio.sleep(1)
            seconds -= 1
        channel = message.channel
        message_id = message.id
        message = await channel.fetch_message(message_id)
        reaction = message.reactions[0]
        users = await reaction.users().flatten()
        user = choice(users)
        await ctx.send(f'Победитель розыгрыша - {user.mention}!\n '
                       f'Напишите {author.mention}, чтобы получить награду')
 
def setup(bot):
	bot.add_cog(giveaway(bot))
