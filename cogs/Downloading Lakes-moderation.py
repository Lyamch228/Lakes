from datetime import datetime
import discord, asyncpg
from discord.ext import commands
from discord import utils
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        if amount == 1:
            await ctx.send(f"Purged {amount} message", delete_after=10)
        else:
            await ctx.send(f"Purged {amount} messages", delete_after=10)
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nick):
        if member == ctx.guild.owner:
            await ctx.send("I can't edit the server owner!")
            return
        if len(nick) > 32:
            await ctx.send("Nickname too long!")
            return
        await member.edit(nick=nick)
        await ctx.send(f"Set nick for {member.name} to {nick}")

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def resetnick(self, ctx, member: discord.Member):
        await member.edit(nick=member.name)  
                          
    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def kick(self, ctx: commands.Context, member: discord.Member, *reason) -> None:
        """
        Kicks the mentioned user from the server
        :param ctx: the message context
        :param member: the member
        :param reason: the reason for the kick
        """
        try:
            await self.bot.kick(member)
            msg = '{} was kicked by {}. Reason: {}'.format(member.name, ctx.message.author.mention, ' '.join(reason))
            send(self.bot, msg, get_channel_by_name(ctx.message.server,
                                                    self.config['aryas']['mod_log_channel_name']))
        except Exception as e:
            print(e)
            send(self.bot, 'Failed to kick ' + member.mention, ctx.message.channel, True)
 
    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def ban(self, ctx: commands.Context, member: discord.Member, *reason) -> None:
        """
        Bans the mentioned user from the server
        :param ctx: The message context
        :param member: The member to be banned
        :param reason: The reason for the ban
        """
        try:
            await self.bot.ban(member)
            msg = '{} was banned by {}. Reason: {}'.format(member.name, ctx.message.author.mention, ' '.join(reason))
            send(self.bot, msg, get_channel_by_name(ctx.message.server,
                                                    self.config['aryas']['mod_log_channel_name']))
        except Exception as e:
            print(e)
            send(self.bot, 'Failed to ban ' + member.mention, ctx.message.channel, True)
 

def setup(bot):
    bot.add_cog(Moderation(bot))
