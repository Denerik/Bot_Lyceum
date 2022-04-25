import discord
from discord.ext import commands
import logging
import requests
import datetime
import os
import json
import random

# Настройки бота
settings = {
    "Name": "Яндекс_Лицей_Бот",
    "Token": "OTY2MzczMzg2OTMyNTg0NTQx.YmAzWQ.UxZ4XonaK-_WsKmcMMXpxbpVIgo",
    "prefix": "-"
}

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True

if not os.path.exists('users.json'):
    with open('users.json', 'w') as file:
        file.write('{}')
        file.close()


# "Тело" Бота
class Yl_Ds_Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.answers = ['Бесспорно', "Предрешено", "Никаких сомнений", "Определённо да", "Можешь быть уверен в этом",
                        "Мне кажется - да", "Вероятнее всего", "Хорошие перспективы", "Знаки говорят - да", "да",
                        "Пока не ясно, попробуй снова", "Спроси позже", "Лучше не рассказывать",
                        "Сейчас нельзя предсказать", "Сконцентрируйся и спроси опять", "Даже не думай",
                        "Мой ответ - нет", "По моим данным — нет", "Перспективы не очень хорошие", "Весьма сомнительно"]
        self.month = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября",
                      "Ноября", "Декабря"]

    # Информация о командах
    @commands.command(name="info")
    async def info(self, ctx):
        embed = discord.Embed(title='Доступные команды:',
                              description='Вы можете получить детальную справку по каждой команде,'
                                          ' выполнив её с -info перед'
                                          ' командой', colour=discord.Colour.purple())
        info = """`-info`"""
        razvlech = """`-coin` `ball8` `cat` `dog`"""
        moderation = """`-ban` `-kick`, '-time'"""
        embed.add_field(name="📋 Информация", value=info, inline=False)
        embed.add_field(name="😄 Развлечения", value=razvlech, inline=False)
        embed.add_field(name="🔧 Утилиты", value=moderation, inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/cLpXGIg.jpg")

        await ctx.send(embed=embed)

    # Рандомная картинка кота
    @commands.command(name="cat")
    async def cat(self, ctx):
        if ctx.author == self.bot.user:
            return
        request = requests.get('https://api.thecatapi.com/v1/images/search').json()
        await ctx.send(request[0]['url'])

    # Рандомная картинка собаки
    @commands.command(name="dog")
    async def dog(self, ctx):
        if ctx.author == self.bot.user:
            return
        request = requests.get('https://dog.ceo/api/breeds/image/random').json()
        await ctx.send(request["message"])

    # Шар судьбы
    @commands.command(name="ball8")
    async def ball8(self, ctx, *question):
        quest = ' '.join(question)
        embed = discord.Embed(description=quest, colour=discord.Colour.purple())
        if ctx.author == self.bot.user:
            return
        if not quest:
            embed.add_field(name='Ошибка:', value=f'Напишите пожалуйста вопрос')
        else:
            embed.add_field(name='Ответ:', value=random.choice(self.answers))
        await ctx.send(embed=embed)

    # Монетка
    @commands.command(name="coin")
    async def coin(self, ctx):
        if ctx.author == self.bot.user:
            return
        embed = discord.Embed(title='Ответ:', description=random.choice(["Орёл", "Решка"]),
                              colour=discord.Colour.purple())
        await ctx.send(embed=embed)

    # дата и время
    @commands.command(name='time')
    async def time(self, ctx):
        if ctx.author == self.bot.user:
            return
        dateandtime = str(datetime.datetime.now()).split()
        date = dateandtime[0].split('-')
        time = dateandtime[1].split(':')
        total = f'{date[2]} {self.month[int(date[1]) - 1]} {date[0]}г     {time[0]}:{time[1]}'
        embed = discord.Embed(title='Дата:', description=total, colour=discord.Colour.purple())
        await ctx.send(embed=embed)

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


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()
            with open('users.json', 'w') as file:
                data[str(member.id)] = {
                    "Name": member.name,
                    "id": member.id,
                    "exp": 0,
                    "level": 1,
                    "need_exp": 15,
                    "warns": 0
                }
                json.dump(data, file, indent=4)
                file.close()


@bot.event
async def on_message(message):
    user = str(message.author.id)
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()
    with open('users.json', 'w') as file:
        need_exp = data[user]['need_exp']
        exp = data[user]['exp']
        if exp >= need_exp:
            data[user]['level'] += 1
            data[user]['need_exp'] *= 2
            reward = f'Поздравляем! вы получили новый {data[user]["level"]} уровень!'
            embed = discord.Embed(title='Поздравляем!', description=reward, colour=discord.Colour.purple())
            await message.channel.send(embed=embed)
        data[user]['exp'] += 3
        json.dump(data, file, indent=4)
        file.close()
    await bot.process_commands(message)


bot.add_cog(Yl_Ds_Bot(bot))
bot.run(settings["Token"])
