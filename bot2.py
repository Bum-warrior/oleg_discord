import discord
import random
import time
import config
from discord import message
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
from urllib.request import *
from bs4 import BeautifulSoup
from discord.utils import get
import ExchangeRate as er
prefix = '$'
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html


def luck_check(arg):
    if arg in config.luck:
        return 50
    else:
        return 50


class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return '{0.author} ударил по жопе {1} потому что *{2}*'.format(ctx, to_slap.mention, argument)


@bot.command()
async def wall(ctx, arg):
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    for i in range(1, 2):
        url = 'https://wallhaven.cc/search?q={}&categories=101&purity=010&sorting=random&order=desc&seed=2PN2e&page='.format(
            arg)
        html = get_html(url + str(i))
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.find_all(class_='preview')
        chosen_image = random.choice(list)
        secondary_html = get_html(chosen_image['href'])
        secondary_soup = BeautifulSoup(secondary_html, 'html.parser')
        image = secondary_soup.find(id='wallpaper')['src']
        urlretrieve(image, image[52:])
        await ctx.send(image)


@bot.command()
async def lr8(ctx, a:int, l:int, v:int, vx:int, t:int):
    ans = (v ** vx * t * 86400) / (a ** l)
    await ctx.send("Вероятность подбора " + str(ans))


@bot.command()
async def num(ctx, high):
    await ctx.send(random.randint(1, high))


@bot.command()
async def rate(ctx):
    rate_dollar = er.get_rate(er.dollar_rub)
    rate_euro = er.get_rate(er.euro_rub)
    emb = discord.Embed(title='{0}'.format("Курс ру*бля* :coin:"), colour=0x58D68D)
    emb.add_field(name="Доллар :dollar:", value=rate_dollar)
    emb.add_field(name="Евро :euro:", value=rate_euro)
    await ctx.send(embed=emb)


@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@bot.command()
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.leave()


@bot.command()
async def history(ctx):
    if str(ctx.message.author) in config.admin:
        max_message = len(bot.cached_messages)
        for i in range(max_message - 2, -1, -1):
            selected_message = bot.cached_messages[i]
            print(str(selected_message.author) + ' ' + str(selected_message.content) + ' ' + str(
                selected_message.channel))
    else:
        await ctx.send('Команда только для администратора бота', delete_after=3)


@bot.command()
async def who(ctx, member: discord.Member):
    if str(member.desktop_status) == "online":
        desctop_smile = ':desktop:'
    else:
        desctop_smile = ':cross:'

    if str(member.mobile_status) == "online":
        mobile_smile = ':iphone:'
    else:
        mobile_smile = ':no_mobile_phones:'

    emb = discord.Embed(title='{0}'.format(member.name), colour=0x58D68D)
    emb.add_field(name="ID", value=member.id)
    emb.add_field(name="Роль", value=member.top_role, inline=False)
    emb.add_field(name='{}'.format(desctop_smile), value=member.desktop_status)
    emb.add_field(name='{}'.format(mobile_smile), value=member.mobile_status)
    emb.add_field(name="Удача", value=str(luck_check(str(member))))
    emb.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=emb)


@bot.command()
async def can(ctx, *, arg):
    await ctx.message.delete()
    proc = random.randint(0, 100)
    if luck_check(str(ctx.message.author)) > proc:
        await ctx.send('Поздравляю, {}, ты удачно смог {}'.format(ctx.message.author.mention, arg, ))
    else:
        await ctx.send('Увы, {}, ты не смог {}'.format(ctx.message.author.mention, arg, ))


@bot.command()
async def roll(ctx):
    await ctx.send('{} твой персонаж {}.'.format(ctx.message.author.mention, random.choice(config.diablo_hero)))


@bot.command()
async def say(ctx, *, arg):
    await ctx.channel.purge(limit=1)
    await ctx.send('{}'.format(arg))


@bot.command()
async def info(ctx):
    emb = discord.Embed(title="Хто я?", colour=0x8E44AD)
    emb.set_author(name='Позвать меня на свой сервер',
                   url='https://discord.com/oauth2/authorize?client_id=752209304156897362&scope=bot&permissions=8')
    emb.set_thumbnail(url='')
    emb.set_image(url=random.choice(config.iam))
    await ctx.send(embed=emb)


@bot.command()
async def help(ctx):
    emb = discord.Embed(title="Немножко о возможностях Олега", colour=0xF4D03F)
    emb.add_field(name=("{}slapthatass *причина*".format(prefix)), value=" :clap: Шлепнуть случайного человека")
    emb.add_field(name=("{}info".format(prefix)), value=" :notebook: Показывает ненужную информацию")
    emb.add_field(name=("{}who".format(prefix)), value=" :spy: Показать информацию о человеке")
    emb.add_field(name=("{}clear *кол-во*".format(prefix)), value=" :cop: Удалить *кол-во* сообщений ")
    emb.add_field(name="{}wall *запрос*".format(prefix), value=" :flower_playing_cards: Случайная пикча по запросу ")
    emb.add_field(name="{}roll".format(prefix), value=":japanese_ogre: Выбрать случайного персонажа Diablo")
    emb.add_field(name='{}can *действие*'.format(prefix), value=':game_die: Проверить свою удачу в *действии*')
    await ctx.send(embed=emb)


@bot.command()
async def helps(ctx):
    emb = discord.Embed(title="В разработке :wrench:")
    emb.add_field(name="{}history".format(prefix), value="Отпечатать историю в консоль")
    await ctx.send(embed=emb)


@bot.command()
async def slapthatass(ctx, *, reason: Slapper):
    if reason == '':
        reason = ' '
    await ctx.send(reason)


@bot.command()
async def boobs(ctx):
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    install_opener(opener)
    emb = discord.Embed()
    emb.set_image(url=random.choice(config.boobs))
    await ctx.send(embed=emb)


@bot.command()
async def clear(ctx, limit=1):
    await ctx.channel.purge(limit=limit)


@bot.event
async def on_ready():
    print('Skynet awake as {0.user}'.format(bot))
    activity = discord.Activity(name='тебя', type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)


@bot.event
@commands.has_permissions(manage_messages=True)
async def on_message(message):
    if message.author == bot.user:
        return

    if 1 == 1:
        print("я получил сообщение " + str(message.author) + str(' ') + str(message.content) + str(
            ' в ') + message.guild.name)

    # for word in config.ban_word:
    #     if word in str(message.content).lower():
    #         await message.delete()
    #         await message.channel.send("А в ебучку {}?".format(message.author.mention), delete_after=2)
    #         return

    # for word in config.gachi:
    #    if word in str(message.content).lower():
    #         await message.channel.send(
    #             "it's ok to be gay {} :gay_pride_flag: ( ͡° ͜ʖ ͡°) :gay_pride_flag:".format(message.author.mention))

    # if str(message.author) == 'As cool as a cucumber#3450':
    #     await message.delete()

    if message.content.startswith('{}hello'.format(prefix)):

        if str(message.author) in config.admin:
            await message.channel.send('здарова, папаша!')
        elif str(message.author) == '1234567890#6035':
            await message.channel.send('привет, кажется тебя зовут артем, не люблю я таких...')
        elif str(message.author) == 'as cool as a cucumber#3450':
            await message.channel.send('привет, ленивая задница!')
        elif str(message.author) == 'nak3z#3029':
            await message.channel.send('здравствуй, одуванчик!')
        elif str(message.author) == 'brilliantman#2713':
            await message.channel.send('сколько лет, сколько зим, рад тебя снова видеть!')
        elif str(message.author) == 'sex police#2843':
            await message.channel.send('оуу, а что это за пряник мне написал? ( ͡° ͜ʖ ͡°)')
        elif str(message.author) == 'grecha#0218':
            await message.channel.send('о, говорят ты срешь за 40 секунд, я твой фанат!')

        else:
            await message.channel.send('а ну тебя, все под ряд меня тыкают...')
        return
    if message.content == ('{}admin'.format(prefix)):
        await message.channel.send(str(config.admin))
        return
    await bot.process_commands(message)

    # @bot.event
    # async def on_reaction_add(reaction, user):
    """
    this is called when a message has a reaction added to it.
    the message is stored in ``reaction.message``.
    for older messages, it's possible that this event
    might not get triggered.
    args:
        reaction:
            a reaction object of the current state of the reaction.
        user:
            an user or member object of the user who added the reaction.
    """
    # print(user, "added", reaction, "to", reaction.message)

    # @bot.event
    # async def on_reaction_remove(reaction, user):
    """
    this is called when a message has a reaction removed from it.
    the message is stored in ``reaction.message``.
    for older messages, it's possible that this event
    might not get triggered.
    args:
        reaction:
            a reaction object of the current state of the reaction.
        user:
            an user or member object of the user who removed the reaction.
    """
    # print(user, "removed", reaction, "from", reaction.message)


@bot.event
async def on_server_join(server):
    print(server, " МЕНЯ СЮДА ЗАКИНУЛИ, ДАВАЙ ДЕЛАТЬ ГРЯЗЮКУ!")


@bot.event
async def on_server_remove(server):
    print("The bot left", server)


bot.run(config.token)
