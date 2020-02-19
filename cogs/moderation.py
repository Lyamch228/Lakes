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
   @commands.command(aliases=['бан'])
   @commands.has_role('Админ')
   async def ban(self, ctx, member: discord.Member = None, reason=None):
	    logs = self.bot.get_channel(id)
	    await ctx.message.delete()
	    if member is None:
	        await ctx.send('Укажите кого надо забанить', delete_after=10)
	    elif member is ctx.message.author:
	        await ctx.send('Ты шо дурной, зачем банить самого себя?', delete_after=10)
	    else:
	        if reason is None:
	            emb = discord.Embed(title='Бан', description=f'Админ {ctx.author.mention} забанил пользователя {member}.')
	            await logs.send(embed=emb)
	            try:
	                await member.send(f'Вас забанили на сервере {ctx.guild.name}')
	            except Exception:
	                print('Ошибочка...')
	            finally:
	                await ctx.guild.ban(member)
	        elif reason is not None:
	            emb = discord.Embed(title='Бан', description=f'Админ {ctx.author.mention} забанил пользователя {member} по причине {reason}.')
	            await logs.send(embed=emb)
	            try:
	                await member.send(f'Вас забанили на сервере {ctx.guild.name} по причине {reason}.')
	            except Exception:
	                print('Ошибочка...')
	            finally:
	                await ctx.guild.ban(member, reason=reason)

def setup(bot):
    bot.add_cog(Moderation(bot))
