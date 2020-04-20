import discord
from discord.ext import commands

import urllib.parse, urllib.request, re

class Youtube_Search(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def youtube(self, ctx, *, search):

		query_string = urllib.parse.urlencode({'search_query': search})
		htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
		search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
		await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

	@commands.Cog.listener()
	@youtube.error
	async def youtube_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Введите фразу, по которой вы хотите найти видео.***')

def setup(bot):
	bot.add_cog(Youtube_Search(bot))