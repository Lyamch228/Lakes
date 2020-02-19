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

    @commands.command(pass_context=True)
    async def kick(self, ctx, user, *, reason=""):
        """Kicks a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                return_msg = "Kicked user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.bot.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.bot.bot_prefix + 'Could not kick user. Not enough permissions.')
        else:
            return await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user.')


    # TODO: Add reason with ban
    @commands.command(aliases=['hban'], pass_context=True)     
    async def hackban(self, ctx, user_id: int):
        """Bans a user outside of the server."""
        author = ctx.message.author
        guild = author.guild

        user = guild.get_member(user_id)
        if user is not None:
            return await ctx.invoke(self.ban, user=user)

        try:
            await self.bot.http.ban(user_id, guild.id, 0)
            await ctx.message.edit(content=self.bot.bot_prefix + 'Banned user: %s' % user_id)
        except discord.NotFound:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user. '
                               'Invalid user ID was provided.')
        except discord.errors.Forbidden:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not ban user. Not enough permissions.')


    @commands.command(pass_context=True)
    async def ban(self, ctx, user, *, reason=""):
        """Bans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                return_msg = "Banned user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.bot.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.bot.bot_prefix + 'Could not ban user. Not enough permissions.')
        else:
            return await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user.')

    @commands.command(aliases=['sban'], pass_context=True)
    async def softban(self, ctx, user, *, reason=""):
        """Bans and unbans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                await ctx.guild.unban(user)
                return_msg = "Banned and unbanned user `{}`".format(user.mention)
                if reason:
                    return_msg += " for reason `{}`".format(reason)
                return_msg += "."
                await ctx.message.edit(content=self.bot.bot_prefix + return_msg)
            except discord.Forbidden:
                await ctx.message.edit(content=self.bot.bot_prefix + 'Could not softban user. Not enough permissions.')
        else:
            return await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user.')   

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
