import discord
from discord.ext import commands

from random import randint

import json
import asyncio

class Levels(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.bot.loop.create_task(self.save_users())
		with open(r'/home/adminroot/vasiliy_bot/cogs/users.json', 'r') as f:
			self.users = json.load(f)

	@commands.Cog.listener()
	async def save_users(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed():
			with open(r'/home/adminroot/vasiliy_bot/cogs/users.json', 'w') as f:
				json.dump(self.users, f, indent=4)

			await asyncio.sleep(5)




	def lvl_up(self, author_id):
		cur_xp = self.users[author_id]['exp']
		cur_lvl = self.users[author_id]['level']

		if cur_xp >= round(4*(cur_lvl**3)/5):
			self.users[author_id]['level'] += 1
			self.users[author_id]['money'] += self.users[author_id]['level']*5
			return True

		else:
			return False



	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return

		author_id = str(message.author.id)

		if not author_id in self.users:
			self.users[author_id] = {}
			self.users[author_id]['level'] = 1
			self.users[author_id]['exp'] = 0
			self.users[author_id]['money'] = 0

		self.users[author_id]['exp'] += 1

		if self.lvl_up(author_id):
			await message.channel.send(f"{message.author.mention} получил {self.users[author_id]['level']} уровень и {self.users[author_id]['level']*5} пивных крышек!")

	@commands.command()
	async def roll(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		await ctx.send(f'{member} роллит {randint(1, 100)}.')

	@commands.command()
	async def level(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('Пользователь не имеет никакого уровня.')
		else:
			embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

			embed.set_author(name=f'Уровень - {member}', icon_url=self.bot.user.avatar_url)

			embed.add_field(name='Уровень', value=self.users[member_id]['level'])
			embed.add_field(name='Опыт', value=self.users[member_id]['exp'])
			embed.add_field(name='Пивные крышки', value=self.users[member_id]['money'])

			await ctx.send(embed=embed)

	@commands.command()
	async def giverole(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['level'] >= 30:
				role = discord.utils.get(member.guild.roles, name='Бро')
				await member.add_roles(role)
				await ctx.send(f'{member}, достигший 30 уровня, получает роль Бро!')
			elif self.users[member_id]['level'] >= 20:
				role = discord.utils.get(member.guild.roles, name='Сотка в кармане')
				await member.add_roles(role)
				await ctx.send(f'{member}, достигший 20 уровня, получает роль Сотка в кармане!')
			elif self.users[member_id]['level'] >= 10:
				role = discord.utils.get(member.guild.roles, name='Местный')
				r_role = discord.utils.get(member.guild.roles, name='Куда сдавать бутылки?')
				await member.add_roles(role)
				await member.remove_roles(r_role)
				await ctx.send(f'{member}, достигший 10 уровня, получает роль Местный!')
			elif self.users[member_id]['level'] < 10:
				await ctx.send('***Повышайте уровень, чтобы получать роли!***')

	#Shop
	@commands.command()
	async def buy1(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['money'] >= 250:
				self.users[member_id]['money'] -= 250
				role = discord.utils.get(member.guild.roles, name='Майнкрафт моя жызнь')
				await member.add_roles(role)
				await ctx.send(f'{member} купил роль Майнкрафт моя жызнь!')
			else:
				await ctx.send('***Недостаточно средств***')

	@commands.command()
	async def buy2(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['money'] >= 500:
				self.users[member_id]['money'] -= 500
				role = discord.utils.get(member.guild.roles, name='20см')
				await member.add_roles(role)
				await ctx.send(f'{member} купил роль 20см!')
			else:
				await ctx.send('***Недостаточно средств***')


	@commands.command()
	async def buy3(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['money'] >= 1000:
				self.users[member_id]['money'] -= 1000
				role = discord.utils.get(member.guild.roles, name='Ярость Любы')
				await member.add_roles(role)
				await ctx.send(f'{member} купил роль Ярость Любы!')
			else:
				await ctx.send('***Недостаточно средств***')


	@commands.command()
	async def buy4(self, ctx, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)

		if not member_id in self.users:
			await ctx.send('***Пользователь не имеет никакого уровня.***')
		else:
			if self.users[member_id]['money'] >= 2000:
				self.users[member_id]['money'] -= 2000
				role = discord.utils.get(member.guild.roles, name='Mod')
				await member.add_roles(role)
				await ctx.send(f'{member} купил роль Mod!')
			else:
				await ctx.send('***Недостаточно средств***')


	#Dice
	@commands.command()
	async def diceup(self, message, amount: int):
		N = int(amount)
		author_id = str(message.author.id)
		if self.users[author_id]['money'] >= N:
			
			roll = randint(0, 100)

			if roll == 0 or roll == 100:
				self.users[author_id]['money'] += N*9
				await message.channel.send(f"❖{roll}❖ {message.author.mention} получил отобый приз в {N*9} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll == 50:
				self.users[author_id]['money'] -= N*5
				await message.channel.send(f"❖{roll}❖ {message.author.mention} получил штраф в {N*5} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll < 50:
				self.users[author_id]['money'] -= N
				await message.channel.send(f"❖{roll}❖ {message.author.mention} проиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll > 50:
				self.users[author_id]['money'] += N
				await message.channel.send(f"❖{roll}❖ {message.author.mention} выиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		else:
			await message.channel.send(f"{message.author.mention}, у тебя недостаточно пивных крышек! ☉{self.users[author_id]['money']}☉")

	@commands.command()
	async def dicedown(self, message, amount: int):
		N = int(amount)
		author_id = str(message.author.id)
		if self.users[author_id]['money'] >= N:
			
			roll = randint(0, 100)

			if roll == 0 or roll == 100:
				self.users[author_id]['money'] += N*9
				await message.channel.send(f"❖{roll}❖ {message.author.mention} получил отобый приз в {N*9} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll == 50:
				self.users[author_id]['money'] -= N*5
				await message.channel.send(f"❖{roll}❖ {message.author.mention} получил штраф в {N*5} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll > 50:
				self.users[author_id]['money'] -= N
				await message.channel.send(f"❖{roll}❖ {message.author.mention} проиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
			elif roll < 50:
				self.users[author_id]['money'] += N
				await message.channel.send(f"❖{roll}❖ {message.author.mention} выиграл в Dice {N} пивные(-ых) крышки(-ек)! ☉{self.users[author_id]['money']}☉")
		else:
			await message.channel.send(f"{message.author.mention}, у тебя недостаточно пивных крышек! ☉{self.users[author_id]['money']}☉")
	

	@commands.Cog.listener()
	@diceup.error
	async def diceup_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!diceup N)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!diceup N)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!diceup N)!***')

	@commands.Cog.listener()
	@dicedown.error
	async def dicedown_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!dicedown N)!***')

	@commands.Cog.listener()
	@buy1.error
	async def buy1_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')

	@commands.Cog.listener()
	@buy2.error
	async def buy2_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')

	@commands.Cog.listener()
	@buy3.error
	async def buy3_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')

	@commands.Cog.listener()
	@buy4.error
	async def buy4_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!buy[index] при покупке себе, member писать не надо)!***')
			
	#Admin commands
	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def addmoney(self, ctx, amount: int, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)
		money = amount

		self.users[member_id]['money'] += money
		await ctx.send(f'{member} получил {money} пивных крышек!')

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def addlvl(self, ctx, amount: int, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)
		lvl = amount

		self.users[member_id]['level'] += lvl
		await ctx.send(f"{member} получил {self.users[member_id]['level']} уровень!")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def addexp(self, ctx, amount: int, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)
		exp = amount

		self.users[member_id]['exp'] += exp
		await ctx.send(f'{member} получил {exp} опыта!')

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def paexp(self, ctx, amount: int, member: discord.Member = None):
		member = ctx.author if not member else member
		member_id = str(member.id)
		exp = amount

		self.users[member_id]['exp'] -= exp
		await ctx.send(f'{member} потерял {exp} опыта!')

	@commands.Cog.listener()
	@addmoney.error
	async def addmoney_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!addmoney сумма @nick#0000***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!addmoney сумма @nick#0000***')

	@commands.Cog.listener()
	@addexp.error
	async def addexp_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!addexp сумма @nick#0000***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!addexp сумма @nick#0000***')

	@commands.Cog.listener()
	@addlvl.error
	async def addlvl_error(self, ctx, error):
		if isinstance(error, commands.CheckFailure):
			await ctx.send('***Вы не имеете права это использовать!***')
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('***Неверно введена команда (!addlvl сумма @nick#0000***')
		if isinstance(error,commands.BadFrgument):
			await ctx.send('***Неверно введена команда (!addlvl сумма @nick#0000***')


def setup(bot):
	bot.add_cog(Levels(bot))
		