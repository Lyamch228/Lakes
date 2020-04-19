#unban.py
#same as ban, but allows a user to be reinvited

import os
import random
import discord 
from discord.ext import commands

class Unban(commands.Cog):
	
	def _init_(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print ('Cog : unban, loaded')

	@commands.command(name='unban')
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, *, member, reason=None):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')

		for ban_entry in banned_users:
			user = ban_entry.user

			if (user.name, user.discriminator) == (member_name, member_discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned {user.mention}')
				return

def setup(client):
	client.add_cog(Unban(client))