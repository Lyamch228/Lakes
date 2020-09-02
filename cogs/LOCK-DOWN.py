import discord
from discord.ext import commands
import datetime
import asyncio
import random

class LD:
 
    def __init__(self, bot):
        self.bot = bot

	
    @commands.group(invoke_without_command=True)
    async def lockdown(self, ctx):
        """Server/Channel lockdown"""
        pass
 
    @lockdown.command(aliases=['channel'])
    async def chan(self, ctx, channel:discord.TextChannel = None, *, reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'channel-lockdown', 0, channel)
        await ctx.send(embed=emb)
    
    @lockdown.command()
    async def server(self, ctx, server:discord.Guild = None, *, reason=None):
        if server is None: server = ctx.guild
        progress = await ctx.send(f'Locking down {server.name}')
        try:
            for channel in server.channels:
                await channel.set_permissions(ctx.guild.default_role, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'server-lockdown', 0, server)
        progress.delete()
        await ctx.send(embed=emb)
 
 
def setup(bot):
	bot.add_cog(LD(bot))
