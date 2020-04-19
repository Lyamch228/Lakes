import os
import random
import discord
from discord.ext import commands

class Ban(commands.Cog):

	def _init_(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Cog : ban, loaded')

	@commands.command(name='ban')
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member : discord.Member, *, reason=None):
		await member.ban(reason=reason)
	#@commands.has_permissions(ban_members=False)
	#async def ban(self, ctx):
	#	await ctx.send('You cannot use this command')

def setup(client):
	client.add_cog(Ban(client))