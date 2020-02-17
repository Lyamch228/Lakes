import discord
from discord.ext import commands

class Example(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):		
		print("я запущен!")
		
def setup(bot):
	bot.add_cog(Example(bot))		