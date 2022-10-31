import discord
import os
import asyncio
from discord.ext import commands
from webserver import keep_alive
intents = discord.Intents.default()
intents.members = True

prefix = os.environ.get("prefix")
token = os.environ.get("token")

#Префикс
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

client.setup = False

# Статусы
@client.event
async def on_ready():
    while True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за срачем"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="музыку для релакса"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ебанатов с сыркафе"))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="пиздец" , url="https://discord.gg/46vYGzeprQ"))
        await asyncio.sleep(20)

# Пинги
@client.command(aliases=["ts"])
async def tsay(ctx, *, message=None):
        message_components = message.split()
        if "@everyone" in message_components or "@here" in message_components:
            await ctx.send("Эй, я запрещаю пинг!")
            return
        await ctx.message.delete()
        await ctx.send(embed=discord.Embed(description= f"{message}", 
                                           color=discord.Colour.random()))

@client.command(aliases=["s"])
async def say(ctx, *, message=None):
        message_components = message.split()
        if "@everyone" in message_components or "@here" in message_components:
            await ctx.send("Эй, я запрещаю пинг!")
            return

        await ctx.message.delete()
        await ctx.send(message)

# Кик
@client.command(aliases=["k"])
@commands.has_permissions(kick_members=True)   
async def kick(context, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await context.send(f'Участник {member} кикнут')

# Бан
@client.command(aliases=["bn"])
@commands.has_permissions(ban_members=True)   
async def ban(context, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await context.send(f'{member} забанен')

# Разбан
@client.command(aliases=["ub"])
@commands.has_permissions(ban_members=True)   
async def unban(context, id : int):
    user = await client.fetch_user(id)
    await context.guild.unban(user)
    await context.send(f'{user.name} теперь разбанен')

# Мут
@client.command(aliases=["m"])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Уборщик")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Мут")

    for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True)

    await member.add_roles(mutedRole)

    embed = discord.Embed(title="Мут", description=f"{member.mention} в  муте.", colour=discord.Colour.light_gray())
    embed.add_field(name="Причина:", value=reason, inline=False)
    embed.add_field(name="Время мута:", value=f"{time} {d}", inline=False)
    await ctx.send(embed=embed)

    if d == "сек":
        mutetime = time

    if d == "мин":
        mutetime = time*60

    if d == "час":
        mutetime = time*60*60

    if d == "день":
        mutetime = time*60*60*24

    with open("TXT_MUTE", "w+") as mutetimef:
        mutetime.write(mutetime)
    
    while True:
        with open("TXT_MUTE", "w+") as mutetimef:
            if int(mutetimef.read()) == 0:
                await member.remove_roles(mutedRole)

                embed = discord.Embed(title="Размут", description=f"Размучен -{member.mention} ", colour=discord.Colour.light_gray())
                await ctx.send(embed=embed)
  
                return
            else:
                mutetime -= 1
                mutetimef.seek(0)
                mutetimef.truncate()
                mutetimef.write(mutetime)
        await asyncio.sleep(1)

keep_alive()
client.run(token)