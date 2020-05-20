import logging
import config as db
 
logging.basicConfig(filename="errorLogs.log", level=logging.ERROR)
 
 
async def is_staff(ctx):
    roles = [role.id for role in ctx.author.roles]
    result = db.guildscol.find_one({"guild": ctx.guild.id})
    if ctx.author.id == ctx.guild.owner or ctx.author.guild_permissions.administrator:
        return True
    if result == []:
        for role in roles:
            if role in ["staff", "mod", "moderator", "admin", "administrator", "owner"]:
                return True
        return False
    for role in result["staffRoles"]:
        if role in roles:
            return True
    for role in result["modRoles"]:
        if role in roles:
            return True
    return False
 
 
async def is_mod(ctx):
    roles = [role.id for role in ctx.author.roles]
    result = db.guildscol.find_one({"guild": ctx.guild.id})
    if result["modRoles"] == []:
        for role in roles:
            if role in ["mod", "moderator", "admin", "administrator", "owner"]:
                return True
        return False
    result = db.guildscol.find_one({"guild": ctx.guild.id})["modRoles"]
    for role in result:
        if role in roles:
            return True
    return False
