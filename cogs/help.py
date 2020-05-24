import discord
import discord, asyncpg
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    
    @commands.command(aliases=['хелп', 'помощь'])
    async def help(self, ctx):
        prefix = '+'
        embed = discord.Embed(title="Все команды **Lake Bot**", description="")
        embed.add_field(name=f'**serverinfo**', value=prefix+"serverinfo показывает информацию о сервере" inline=True)  # Создает строку
        embed.add_field(name=f'**userinfo**', value=prefix+"userinfo показвает информацию об участнике", inline=True)  # Создает строку
        embed.add_field(name=f'**tempmute**', value=prefix+"tempmute <юзер>", inline=True)  # Создает строку
        embed.add_field(name=f'**mute**', value=prefix+"mute <юзер>", inline=True)  # Создает строку
        embed.add_field(name=f'**Шар**', value=prefix+"шар <вопрос>", inline=True)  # Создает строку
        embed.add_field(name=f'**ban**', value=prefix+"ban <юзер>", inline=True)  # Создает строку
        embed.add_field(name=f'**kick**', value=prefix+"kick <юзер>", inline=True)  # Создает строку
        embed.add_field(name=f'**kick**', value=prefix+"kick <юзер>", inline=True) # Создает строку
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
