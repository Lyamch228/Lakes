import discord
import random
import requests
import nekos
from discord.ext import commands

nekos1 = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', '8ball', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'ero', 'smug', 'goose', 'baka', 'woof']


class NSFW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    


    @commands.command(aliases=['n'])
    async def nekos(self, ctx, arg=None):
        await ctx.message.delete()

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"


        if channel_nsfw:

            if arg == None:
                emb = discord.Embed(title = ':flushed: NSFW', url = nekos.img(random.choice(nekos1)))
                emb.set_image(url=nekos.img(random.choice(nekos1)))
                emb.set_footer( text = 'Если не работает, тыкай NSFW!')
                await ctx.send(embed=emb, delete_after = 60)
                #await ctx.send(random_post.url)

                return
            


            emb = discord.Embed(title = ':flushed: NSFW', url = nekos.img(f'{arg}')	)
            emb.set_image(url=nekos.img(f'{arg}'))
            emb.set_footer( text = 'Если не работает, тыкай NSFW!')
            await ctx.send(embed=emb, delete_after = 60)
            #await ctx.send(random_post.url)
        else:
            emb = discord.Embed(title = ':flushed: Ты не можешь использовать эту команду здесь!')
            await ctx.send( embed = emb, delete_after = 30)

def setup(bot):
    bot.add_cog(NSFW(bot))
