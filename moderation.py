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
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member is None:
            await ctx.send("Who do you want to unban?")
        banned_users = await ctx.guild.bans()
        try:
            member_name, member_discriminator = member.split("#")
        except ValueError:
            await ctx.send("invalid member")
            return
        for ban_entry in banned_users:
            if (ban_entry.user.name, ban_entry.user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f"Unbanned {ban_entry.user.name}")
                channel = discord.utils.get(ctx.guild.text_channels, name="member_logs")
                embed = discord.Embed(description=f"{ban_entry.user.name}#{ban_entry.user.discriminator} ", colour=discord.Color.green(), timestamp=datetime.utcnow())
                embed.set_thumbnail(url=ban_entry.user.avatar_url)
                embed.set_footer(text=f"User ID:{ban_entry.user.id}")
                embed.set_author(name=f"{ban_entry.user.name} got unbanned from the server", icon_url=ban_entry.user.avatar_url)
                await channel.send(embed=embed)
                return
        # await ctx.send("Member couldnt be found or isnt banned")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.ban_members:
            await ctx.send('That member is Admin/Staff, I can\'t do that!')
            return
        if member == ctx.author:
            await ctx.send('You can\'t ban yourself!')
        await ctx.guild.ban(user=member, reason=reason, delete_message_days=7)
        await ctx.send(f"Banned {member.mention}!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if member.guild_permissions.kick_members:
            await ctx.send('That member is Admin/Staff, I can\'t do that!')
            return
        if member == ctx.author:
            await ctx.send('You can\'t kick yourself!')
        await ctx.guild.kick(user=member, reason=reason, delete_message_days=7)
        await ctx.send(f"kicked {member.mention}!")
        

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

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def referralban(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Referral Banned")
        if role is None:
            await ctx.send("No role called 'Referral Banned' found")
            return
        if role in member.roles:
            await ctx.send("Member is already Referral Banned!")
            return
        await member.add_roles(role)
        await ctx.send(f"Referral Banned {member.name}")

def setup(bot):
    bot.add_cog(Moderation(bot))
