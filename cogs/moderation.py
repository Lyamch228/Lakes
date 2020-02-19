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
        await member.edit(nick=member.name   
                          
    @commands.command(aliases=["banish"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Sinner=None, reason=None):
        """Casts users out of heaven."""
        
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")
        
        try: # Tries to ban user
            await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await ctx.send(f"{user.mention} was cast out of heaven for {reason}.")
        except discord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")
    
    @commands.command()
    async def kick(self, ctx, user: Sinner=None, reason=None):
        if not user: # checks if there is a user 
            return await ctx.send("You must specify a user")
        
        try: # tries to kick user
            await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
        except discord.Forbidden:
            return await ctx.send("Are you trying to kick someone higher than the bot?")

def setup(bot):
    bot.add_cog(Moderation(bot))
