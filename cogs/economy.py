from discord.ext import commands

import discord
import json


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = "cogs\\library\\misc\\economy-data.json"

    async def withdraw(self, member, amount):
        data = get_data(self.path)
        member_id = str(member.id)

        current_amount = float(data[member_id]["balance"])
        data[member_id]["balance"] = str(current_amount - amount)

        save_data(self.path, data)

    async def deposit(self, member, amount):
        data = get_data(self.path)
        member_id = str(member.id)

        current_amount = float(data[member_id]["balance"])
        data[member_id]["balance"] = str(current_amount + amount)

        save_data(self.path, data)

    async def new_user(self, member):
        data = get_data(self.path)
        member_id = str(member.id)

        if member_id in data:
            pass
        else:
            data[member_id] = {
                "balance": "1000",
                "member-name": member.name
            }
            save_data(self.path, data)

    def get_balance(self, member):
        data = get_data(self.path)
        member_id = str(member.id)
        balance = float(data[member_id]["balance"])
        return balance

    @commands.command(name="balance")
    async def show_balance(self, ctx):
        author = ctx.author
        current_amount = Economy.get_balance(self, author)

        await ctx.send(f"{author.mention}, your balance is ${current_amount}")

    @commands.command(name="initialize")
    @commands.has_any_role("Moderator", "Server Owner")
    async def _initialize(self, ctx):
        members = ctx.guild.members
        data = {}

        for member in members:
            data[member.id] = {
                "member-name": member.name,
                "balance": "1000"
            }

        with open(self.path, "w") as file:
            json.dump(data, file, indent=2, sort_keys=True)


def get_data(path):
    with open(path) as file:
        data = json.load(file)
        return data


def save_data(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4, sort_keys=True)


def setup(bot):
    bot.add_cog(Economy(bot))