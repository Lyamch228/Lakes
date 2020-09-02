import discord
from discord.ext import commands
import datetime
import asyncio
import random

class Mod:
 
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def mute(self, ctx, member:discord.Member, duration, *, reason=None):
        '''Denies someone from chatting in all text channels and talking in voice channels for a specified duration'''
        unit = duration[-1]
        if unit == 's':
            time = int(duration[:-1])
            longunit = 'seconds'
        elif unit == 'm':
            time = int(duration[:-1]) * 60
            longunit = 'minutes'
        elif unit == 'h':
            time = int(duration[:-1]) * 60 * 60
            longunit = 'hours'
        else:
            await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
            return
 
        progress = await ctx.send('Muting user!')
        try:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
 
            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
        except:
            success = False
        else:
            success = True
 
        emb = await self.format_mod_embed(ctx, member, success, 'mute', f'{str(duration[:-1])} {longunit}')
        progress.delete()
        await ctx.send(embed=emb)
        await asyncio.sleep(time)
        try:
            for channel in ctx.guild.channels:
                await channel.set_permissions(member, overwrite=None, reason=reason)
        except:
            pass
            
    
    @commands.command()
    async def unmute(self, ctx, member:discord.Member, *, reason=None):
        '''Removes channel overrides for specified member'''
        progress = await ctx.send('Unmuting user!')
        try:
            for channel in ctx.message.guild.channels:
                await channel.set_permissions(member, overwrite=None, reason=reason)
        except:
            success = False
        else:
            success = True
            
        emb = await self.format_mod_embed(ctx, member, success, 'unmute')
        progress.delete()
        await ctx.send(embed=emb)
 
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
	bot.add_cog(Mod(bot))
