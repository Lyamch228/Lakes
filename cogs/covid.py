import discord, asyncpg
from discord.ext import commands
import json
import requests

class commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['коронавирус', 'ковид'])
    async def covid(self, ctx, country):
        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == country: 
                embed = discord.Embed(title=f'Статистика Коронавируса | {country}')
                embed.add_field(name='Выздоровело:',          value=f'{item["recovered"]} человек')
                embed.add_field(name='Заболеваний:',          value=f'{item["cases"]} человек')
                embed.add_field(name='Погибло:',              value=f'{item["deaths"]} человек')
                embed.add_field(name='Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                embed.add_field(name='Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
                embed.add_field(name='Проведено тестов:',     value=f'{item["tests"]} человек')
                embed.add_field(name='Активные зараженные:',  value=f'{item["active"]} человек')
                embed.add_field(name='В тяжелом состоянии:',  value=f'{item["critical"]} человек')
                embed.set_thumbnail(url=item["countryInfo"]['flag'])
                embed.set_footer(text="Информация о вирусе")

                return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(commands(bot))
