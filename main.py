import discord
from discord.ext import commands
import logging
import requests

# Настройки бота
settings = {
    "Name": "Яндекс_Лицей_Бот",
    "Token": "OTY2MzczMzg2OTMyNTg0NTQx.YmAzWQ.UxZ4XonaK-_WsKmcMMXpxbpVIgo",
    "prefix": "-"
}

# Логинг
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True


# "Тело" Бота
class Yl_Ds_Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Информация о командах
    @commands.command(name="info")
    async def info(self, ctx):
        embed = discord.Embed(title='Доступные команды:',
                              description='Вы можете получить детальную справку по каждой команде,'
                                          ' выполнив её с -info перед'
                                          ' командой', colour=discord.Colour.purple())
        info = """`-info`"""
        razvlech = """`-coin` `8ball` `cat` `dog`"""
        moderation = """`-ban` `-kick`"""
        embed.add_field(name="📋 Информация", value=info, inline=False)
        embed.add_field(name="😄 Развлечения", value=razvlech, inline=False)
        embed.add_field(name="🔧 Модерация", value=moderation, inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/cLpXGIg.jpg")

        await ctx.send(embed=embed)

    # Рандомная картинка кота
    @commands.command(name="cat")
    async def cat(self, ctx):
        author = ctx.author
        if author == self.bot.user:
            return
        request = requests.get('https://api.thecatapi.com/v1/images/search').json()
        await ctx.send(request[0]['url'])

    # Рандомная картинка собаки
    @commands.command(name="dog")
    async def dog(self, ctx):
        author = ctx.author
        if author == self.bot.user:
            return
        request = requests.get('https://dog.ceo/api/breeds/image/random').json()
        await ctx.send(request["message"])

    # Бан пользователя
    @commands.command(name="ban")
    async def ban(self, ctx, user: discord.Member):
        await user.ban()
        retStr = f"""```fix\nПользователь {user} был забанен```"""
        embed = discord.Embed(title='Отчёт', colour=discord.Colour.purple())
        embed.add_field(name='Бан', value=retStr)
        await ctx.send(embed=embed)

    # Кик пользователя
    @commands.command(name="kick")
    async def kick(self, ctx, user: discord.Member):
        retStr = f"""```Пользователь {user} был кикнут```"""
        info = """`-хелп` `-инфо`"""
        embed = discord.Embed(title='Отчёт', description=retStr, colour=discord.Colour.purple())
        embed.add_field(name="📋Информация", value=info)
        await ctx.send(embed=embed)


bot = commands.Bot(command_prefix=settings["prefix"], intents=intents)

bot.add_cog(Yl_Ds_Bot(bot))
bot.run(settings["Token"])
