import discord
from discord.ext import commands
import datetime
import checks
import config as db
from asyncio import TimeoutError
 
 
class Moderation:
    def __init__(self, bot):
        self.bot = bot
 
    @commands.guild_only()
    @commands.command()
    async def warn(self, ctx, user: discord.User, *, warning: str):
        if (await checks.is_staff(ctx)):
            if (user == ctx.author):
                await ctx.send("<:no:484017898730291211>You cannot warn yourself, that would be silly!")
            elif (len(warning) > 500):
                await ctx.send(f"<:no:484017898730291211>The maximum length of a warning is 500 characters (including spaces and punctuation)\nYou "
                               f"used {len(warning)} characters")
                return
            else:
                result = db.memberscol.find_one({"guild": ctx.guild.id, "user": user.id})
                if (result is None):
                    result = {"guild": ctx.guild.id, "user": user.id, "warnings":
                              [{"warning": warning, "time": datetime.datetime.utcnow(), "warner": ctx.author.id}]}
                else:
                    result["warnings"].append({"warning": warning, "time": datetime.datetime.utcnow(), "warner": ctx.author.id})
                    if len(result["warnings"]) > 30:
                        await ctx.send("<:no:484017898730291211>Iris has a limit of 30 warnings per member. There's a good reason for this!")
                        return
                db.memberscol.replace_one({"guild": ctx.guild.id, "user": user.id}, result, True)
                serversettings = db.guildscol.find_one({"guild": ctx.guild.id})
                embed = discord.Embed(title="", description=f"Warned <@{user.id}>\n**Warning:** `{warning}`", colour=0x00988E, timestamp=datetime.
                                      datetime.utcnow())
                embed.set_footer(text=f"By {ctx.author}", icon_url=ctx.author.avatar_url_as())
                if serversettings["warningLimit"] is not None:
                    if len(result["warnings"]) >= serversettings["warningLimit"]:
                        limit = serversettings["warningLimit"]
                        if serversettings["warningAction"] == "ban":
                            user.ban(reason=f"Warning count is greater than {limit}.")
                            embed.set_footer(text=f"By {ctx.author}, banned this user.", icon_url=ctx.author.avatar_url_as())
                        elif serversettings["warningAction"] == "kick":
                            user.kick(reason=f"Warning count is greater than {limit}.")
                            embed.set_footer(text=f"By {ctx.author}, kicked this user.", icon_url=ctx.author.avatar_url_as())
                        elif serversettings["warningAction"] == "mute":
                            role = discord.utils.get(ctx.guild.roles, id=serversettings["muteRole"])
                            await user.add_roles(reason="Muted for maximum warnings reached.", roles=[role])
                embed.set_author(name="New warning", icon_url=user.avatar_url_as())
                await ctx.send(embed=embed)
 
    @warn.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}warn `@<user>` `<warning>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a warning to a user. The warning can be up to 500 characters long. Requires a staff role, mod"
                                                "role, ban permissions, administrative permissions or owner permissions to warn a user.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def warnings(self, ctx, user: discord.User=None, page: int=1):
        if user is None:
            user = ctx.author
        if (ctx.author.id == user.id or await checks.is_staff(ctx)):
            start = page*5-5
            end = page*5
            warnings = ""
            post = f"Warnings for {user} ({user.id}). Requested by {ctx.author}:\n---------------------------------\n"
            result = db.memberscol.find_one({"user": user.id, "guild": ctx.guild.id})
            try:
                result["warnings"]
            except Exception:
                result = {"warnings": []}
            if (result["warnings"] != []):
                counter = page*5-5
                for warning in result["warnings"][start:end]:
                    counter += 1
                    warner = await self.bot.get_user_info(warning["warner"])
                    timestamp = warning["time"]
                    warningText = warning["warning"]
                    post = f"{post}{warningText}\nBy: {warner}\nDate: D/M/Y {timestamp.day}/{timestamp.month}/{timestamp.year}\n------------\n"
                    if (len(warning["warning"]) > 300):
                        warningStr = warning["warning"][:230]
                        warnings = f"{warnings}**{counter}.** `{warningStr}...` | By: {warner} | {timestamp.day}/{timestamp.month}/"\
                                   f"{timestamp.year}\n\n"
                    else:
                        warningStr = warning["warning"]
                        warnings = f"{warnings}**{counter}.** `{warningStr}` | By: {warner} | {timestamp.day}/{timestamp.month}/{timestamp.year}"\
                                   f"\n\n"
            elif warnings == "" and page != 1:
                await ctx.send("<:no:484017898730291211>Unkown page.")
                return
            else:
                warnings = f"`{user}` has no warnings in this server"
                embed = discord.Embed(title="", description=warnings, timestamp=datetime.datetime.utcnow(), colour=0x00988E)
                embed.set_author(name=f"Warnings for {user}", icon_url=user.avatar_url_as())
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url_as())
                await ctx.send(embed=embed)
                return
            embed = discord.Embed(title="", description=warnings, timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_author(name=f"Warnings for {user}", icon_url=user.avatar_url_as())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url_as())
            await ctx.send(embed=embed)
 
    @warnings.error
    async def warnings_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="", description=f"• {ctx.prefix}warnings <@user> <page>\n"
                                                        f"• {ctx.prefix}warnings list <@user> [page]\n"
                                                        f"• {ctx.prefix}warnings add <@user> <warning>\n"
                                                        f"• {ctx.prefix}warnings delete <@user> <warning id>\n"
                                                        f"• {ctx.prefix}warnings clear <@user>", colour=0x00988E)
            embed.set_footer(text="<Required> [Optional]")
            embed.set_author(name="Command help", icon_url=self.bot.user.avatar_url)
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
 
    @commands.guild_only()
    @warnings.command(aliases=["warn", "addwarning", "warnuser", "warningadd", "warnadd", "addwarn"])
    async def add(self, ctx, user: discord.Member=None, *, warning: str=None):
        if (await checks.is_staff(ctx)):
            if (user == ctx.author):
                await ctx.send("<:no:484017898730291211>You cannot warn yourself, that would be silly!")
            elif (len(warning) > 500):
                await ctx.send(f"<:no:484017898730291211>The maximum length of a warning is 500 characters (including spaces and punctuation)\nYou "
                               f"used {len(warning)} characters")
                return
            else:
                result = db.memberscol.find_one({"guild": ctx.guild.id, "user": user.id})
                if (result is None):
                    result = {"guild": ctx.guild.id, "user": user.id, "warnings":
                              [{"warning": warning, "time": datetime.datetime.utcnow(), "warner": ctx.author.id}]}
                else:
                    result["warnings"].append({"warning": warning, "time": datetime.datetime.utcnow(), "warner": ctx.author.id})
                    if len(result["warnings"]) > 30:
                        await ctx.send("<:no:484017898730291211>Iris has a limit of 30 warnings per member. There's a good reason for this!")
                        return
                db.memberscol.replace_one({"guild": ctx.guild.id, "user": user.id}, result, True)
                serversettings = db.guildscol.find_one({"guild": ctx.guild.id})
                embed = discord.Embed(title="", description=f"Warned <@{user.id}>\n**Warning:** `{warning}`", colour=0x00988E, timestamp=datetime.
                                      datetime.utcnow())
                embed.set_footer(text=f"By {ctx.author}", icon_url=ctx.author.avatar_url_as())
                if serversettings["warningLimit"] is not None:
                    if len(result["warnings"]) >= serversettings["warningLimit"]:
                        limit = serversettings["warningLimit"]
                        if serversettings["warningAction"] == "ban":
                            user.ban(reason=f"Warning count is greater than {limit}.")
                            embed.set_footer(text=f"By {ctx.author}, banned this user.", icon_url=ctx.author.avatar_url_as())
                        elif serversettings["warningAction"] == "kick":
                            user.kick(reason=f"Warning count is greater than {limit}.")
                            embed.set_footer(text=f"By {ctx.author}, kicked this user.", icon_url=ctx.author.avatar_url_as())
                        elif serversettings["warningAction"] == "mute":
                            try:
                                role = discord.utils.get(ctx.guild.roles, id=serversettings["muteRole"])
                            except Exception:
                                pass
                            await user.add_roles(reason="Muted for maximum warnings reached.", roles=[role])
                embed.set_author(name="New warning", icon_url=user.avatar_url_as())
                await ctx.send(embed=embed)
 
    @add.error
    async def add_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}warn `@<user>` `<warning>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a warning to a user. The warning can be up to 500 characters long. Requires a staff role, mod"
                                                "role, ban permissions, administrative permissions or owner permissions to warn a user.")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @warnings.group(aliases=["list", "listwarns", "warnlist"])
    async def listwarnings(self, ctx, user: discord.User=None, page: int=1):
        if (ctx.author.id == user.id or await checks.is_staff(ctx)):
            start = page*5-5
            end = page*5
            warnings = ""
            post = f"Warnings for {user} ({user.id}). Requested by {ctx.author}:\n---------------------------------\n"
            result = db.memberscol.find_one({"user": user.id, "guild": ctx.guild.id})
            try:
                result["warnings"]
            except Exception:
                result = {"warnings": []}
            if (result["warnings"] != []):
                counter = page*5-5
                for warning in result["warnings"][start:end]:
                    counter += 1
                    warner = await self.bot.get_user_info(warning["warner"])
                    timestamp = warning["time"]
                    warningText = warning["warning"]
                    post = f"{post}{warningText}\nBy: {warner}\nDate: D/M/Y {timestamp.day}/{timestamp.month}/{timestamp.year}\n------------\n"
                    if (len(warning["warning"]) > 300):
                        warningStr = warning["warning"][:230]
                        warnings = f"{warnings}**{counter}.** `{warningStr}...` | By: {warner} | {timestamp.day}/{timestamp.month}/"\
                                   f"{timestamp.year}\n\n"
                    else:
                        warningStr = warning["warning"]
                        warnings = f"{warnings}**{counter}.** `{warningStr}` | By: {warner} | {timestamp.day}/{timestamp.month}/{timestamp.year}"\
                                   f"\n\n"
            elif warnings == "" and page != 1:
                await ctx.send("<:no:484017898730291211>Unkown page.")
                return
            else:
                warnings = f"`{user}` has no warnings in this server"
            embed = discord.Embed(title="", description=warnings, timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_author(name=f"Warnings for {user}", icon_url=user.avatar_url_as())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url_as())
            await ctx.send(embed=embed)
 
    @listwarnings.error
    async def listwarnings_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}warnings list `@<user>` `[page]`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Lists a user's warnings. Requires a staff role, mod role, ban permissions, administrative"
                                                " permissions or owner permissions to view others' warnings.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @warnings.group(aliases=["remove", "del", "erase", "delwarning", "delwarn", "warndel", "warningdel"])
    async def delete(self, ctx, user: discord.User, warning: int):
        if (ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator or await checks.is_mod(ctx)):
            try:
                warning = int(warning)
                result = db.memberscol.find_one({"user": user.id, "guild": ctx.guild.id})
                if result["warnings"] is None:
                    result["warnings"] = []
                if (warning > len(result["warnings"])):
                    await ctx.send(f"<:no:484017898730291211>Sorry, that user doesn't have a warning with the id `{warning}`")
                    return
                timestamp = result["warnings"][warning-1]["time"]
                warningStr = result["warnings"][warning-1]["warning"]
                warner = await self.bot.get_user_info(result["warnings"][warning-1]["warner"])
                del result["warnings"][warning-1]
                db.memberscol.replace_one({"guild": ctx.guild.id, "user": user.id}, {"guild": ctx.guild.id, "user": user.id,
                                                                                     "warnings": result["warnings"]})
                embed = discord.Embed(title="", description=f"Warning: `{warningStr}` | By: {warner} | {timestamp.day}/{timestamp.month}/"
                                                            f"{timestamp.year}\n\n",
                                      timestamp=datetime.datetime.utcnow(), colour=0x00988E)
                embed.set_footer(text=f"By {ctx.author}({ctx.author.id})", icon_url=ctx.author.avatar_url_as())
                embed.set_author(name="Deleted warning", icon_url=user.avatar_url_as())
                await ctx.send(embed=embed)
 
            except ValueError:
                await ctx.send(f"<:no:484017898730291211>You must supply a number corresponding to a warning, not text.")
                return
 
    @delete.error
    async def delete_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}warnings delete `@<user>` `<warning id>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes a single warning from a user. Requires a mod role, ban permissions, administrative "
                                                "permissions, or owner permissions to delete a warning.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @warnings.group(aliases=["clean", "clearwarnings", "clearwarns", "warningsclear", "warnsclear"])
    async def clear(self, ctx, user: discord.User=None):
        if (ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator or await checks.is_mod(ctx)):
            result = db.memberscol.find_one({"user": user.id, "guild": ctx.guild.id})
            try:
                if (result["warnings"] == []):
                    await ctx.send(f"<:no:484017898730291211>`{user}` has no warnings to clear.")
                    return
            except Exception:
                await ctx.send(f"<:no:484017898730291211>`{user}` has no warnings to clear.")
                return
            msg = await ctx.send(f"Are you sure you would like to remove **all** `{user}`'s warnings? `(y/n)`")
 
            def check(message):
                content = message.content.lower()
                if (message.channel == ctx.channel and message.author == ctx.author and content in ["yes", "y"]):
                    return True
                elif (message.channel == ctx.channel and message.author == ctx.author and content in ["no", "n"]):
                    return False
            try:
                await self.bot.wait_for("message", check=check, timeout=60)
            except TimeoutError:
                await msg.edit(content="<:no:484017898730291211>Timed out.", delete_after=20)
                return
            db.memberscol.delete_many({"user": user.id, "guild": ctx.guild.id})
            embed = discord.Embed(title="", description=f"**Warnings: ** ", timestamp=datetime.datetime.
                                  utcnow(), colour=0x00988E)
            embed.set_author(name=f"Removed all {user.name}#{user.discriminator}'s warnings.", icon_url=self.bot.user.avatar_url)
            embed.set_footer(text=f"Removed by {ctx.author}", icon_url=ctx.author.avatar_url_as())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211> {ctx.author.mention} You do not have permission to do that.")
 
    @commands.guild_only()
    @commands.group(invoke_without_command=True, aliases=["purgemessages", "purgemsgs", "prune"])
    async def purge(self, ctx, amount: int):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 2000:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 2000 messages at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def defaultCheck(message):
                        return message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, check=defaultCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @purge.error
    async def purge_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Indiscriminately purges messages in a channel. The messages must be newer than 14 days. Requires "
                                                "`DELETE_MESSAGES` permission.")
            embed.add_field(name="Subcommands:", value=f"""**N.B.** All purge commands only delete messages newer than 14 days. (Subcommands limit amount to 200)
            {ctx.prefix}purge user `@<user>` `<amount>` - Deletes messages sent by the specified user.
            {ctx.prefix}purge bots `<amount>` - Deletes messages sent by bots.
            {ctx.prefix}purge contains `<text>` `<amount>` - Deletes messages containing the specified text.
            {ctx.prefix}purge embed `<amount>` - Deletes messages containing Embeds.
            {ctx.prefix}purge startswith `<text>` `<amount>` - Deletes messages starting with the specified text.
            {ctx.prefix}purge endswith `<text>` `<amount>` - Deletes messages ending with the specified text.
            {ctx.prefix}purge notcontains `<text>` `<amount>` - Deletes messages not containing the specified text.
            {ctx.prefix}purge mentions `@<user>` `<amount>` - Deletes messages mentioning the specified user.""")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["user"])
    async def member(self, ctx, user: discord.User, amount: int):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def userCheck(message):
                            return message.author == user and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=userCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages by {user} in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @member.error
    async def purge_member_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge member `@<user>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages sent by the specified user. The messages must be newer than 14 days. "
                                                "Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["bot"])
    async def bots(self, ctx, amount: int):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def botCheck(message):
                        return message.author.bot and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=botCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages by bots in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @bots.error
    async def purge_bots_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge bots `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages sent by bots. The messages must be newer than 14 days. "
                                                "Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["contents"])
    async def contains(self, ctx, *args):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            try:
                amount = int(args[-1])
            except Exception:
                await ctx.send("<:no:484017898730291211>You must supply a valid content and amount of messages.")
                return
            content = " ".join(args[:-1])
            if ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.ban_members or await checks.is_staff(ctx):
                if amount > 200:
                    await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
                else:
                    async with ctx.typing():
                        alpha = datetime.datetime.now()
                        twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                        def contentCheck(message):
                            return content in message.content and message.created_at > twoweeksago
                        purged = await ctx.channel.purge(limit=amount, bulk=True, check=contentCheck)
                        time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                        embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages containing "
                                                                    f"`{content.replace('`', '')}` in {time}ms",
                                              colour=0x00988E)
                        embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                        await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @contains.error
    async def purge_contains_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge contains `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages containing the specified text. The messages must be newer than 14 days. "
                                                "Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["embeds"])
    async def embed(self, ctx, amount: int):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def embedCheck(message):
                        return message.embeds and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=embedCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages containing embeds in "
                                                                f"{time}ms", colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @embed.error
    async def purge_embed_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge bots `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages containing Embeds. The messages must be newer than 14 days. "
                                                "Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["startswith", "prefix"])
    async def beginswith(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge startswith `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages starting with the specified text. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            await ctx.send(embed=embed)
            return
        try:
            amount = int(args[-1])
        except Exception:
            await ctx.send("<:no:484017898730291211>You must supply a valid content and amount of messages.")
            return
        content = " ".join(args[:-1])
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def startCheck(message):
                        return message.content.startswith(content) and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=startCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages starting with "
                                                                f"{content.replace('`', '')} in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @beginswith.error
    async def purge_beginswith_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge startswith `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages starting with the specified text. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["endswith", "suffix"])
    async def finisheswith(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge endswith `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages ending with the specified text. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            await ctx.send(embed=embed)
            return
        try:
            amount = int(args[-1])
        except Exception:
            await ctx.send("<:no:484017898730291211>You must supply a valid content and amount of messages.")
            return
        content = " ".join(args[:-1])
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def endCheck(message):
                        return message.content.endswith(content) and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=endCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages ending with "
                                                                f"{content.replace('`', '')} in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @finisheswith.error
    async def purge_finisheswith_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge endswith `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages ending with the specified text. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["not", "doesn't contain", "nocontains"])
    async def notcontains(self, ctx, *args):
        try:
            amount = int(args[-1])
        except Exception:
            await ctx.send("<:no:484017898730291211>You must supply a valid content and amount of messages.")
            return
        content = " ".join(args[:-1])
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def notCheck(message):
                        return content not in message.content and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=notCheck)
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages not containing "
                                                                f"{content.replace('`', '')} in {time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @notcontains.error
    async def purge_notcontains_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge notcontains `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages not containing text. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @purge.command(aliases=["mentionsuser", "mentionsmember"])
    async def mentions(self, ctx, user: discord.User, amount: int):
        if (ctx.channel.permissions_for(ctx.author).manage_messages):
            if amount > 200:
                await ctx.send("<:no:484017898730291211>I can purge a maximum of 200 messages conditionally at once.")
            else:
                async with ctx.typing():
                    alpha = datetime.datetime.now()
                    twoweeksago = datetime.datetime.utcnow() - datetime.timedelta(days=14)
 
                    def contentCheck(message):
                        return user in message.mentions and message.created_at > twoweeksago
                    purged = await ctx.channel.purge(limit=amount, bulk=True, check=contentCheck, after=datetime.datetime.utcnow() -
                                                     datetime.timedelta(days=14))
                    time = round((datetime.datetime.now() - alpha).total_seconds()*100)
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Deleted {len(purged)} messages mentioning {user} in "
                                                                f"{time}ms",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}", icon_url=ctx.author.avatar_url_as())
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"<:no:484017898730291211>You do not have the `MANAGE_MESSAGES` permission.")
 
    @mentions.error
    async def purge_mentions_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}purge notcontains `<text>` `<amount>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Deletes up to 200 messages mentioning the specified user. The messages must be newer than 14 "
                                                "days. Requires `DELETE_MESSAGES` permission.")
            embed.set_footer(text="<Required> [Optional]")
            try:
                await ctx.send(embed=embed)
            except Exception:
                pass
        elif isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>You do not have `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
        elif isinstance(error, commands.BotMissingPermissions):
            try:
                await ctx.send(f"<:no:484017898730291211>The bot requires `{', '.join(error.missing_perms)}` permissions.")
            except Exception:
                pass
 
    @commands.guild_only()
    @commands.command(aliases=["muteuser", "mute-user"])
    async def mute(self, ctx, user: discord.Member, time=None):
        if await checks.is_staff(ctx):
            if time is None:
                result = db.guildscol.find_one({"guild": ctx.guild.id})
                if result["muteRole"] is not None:
                    role = discord.utils.get(ctx.guild.roles, id=result["muteRole"])
                    print("test")
                    await user.add_roles(role, reason=f"Muted by {ctx.author}")
                    await ctx.send(f"<:yes:484017899065835521>Muted {ctx.author}")
                else:
                    await ctx.send(f"<:no:484017898730291211>You need to setup the mute role with `{ctx.prefix}settings muterole <@role | role | "
                                   f"remove>`")
                    return
            elif time is not None:
                time = datetime.datetime.strptime(time, "%Mm %Hh %dd %mm")
                print(time)
                time = time - datetime.datetime.now()
                db.mutescol.replace_one({"user": user.id, "guild": ctx.guild.id}, {"user": user.id, "guild": ctx.guild.id, "time": time}, True)
            else:
                await ctx.send("<:no:484017898730291211>You are lacking staff permission.")
 
 
def setup(bot):
    bot.add_cog(Moderation(bot))
