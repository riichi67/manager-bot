import discord
import os
from discord.ext import commands
from webserver import keep_alive

prefix = os.environ.get("prefix")
token = os.environ.get("token")
bot = discord.Bot()

@bot.event
async def on_ready():
  print(f'{bot.user.name} запустился и готов к работе!')

@bot.slash_command(description = 'Заставит кого угодно замолчать.') # Мьют
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Уборщик")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Уборщик")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    await member.add_roles(mutedRole)
    await ctx.respond(f"Мьют успешно выдан участнику {member.mention}!")

@bot.slash_command(description = 'Любому молчанию должен прийти конец, не так ли?') # Размьют
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Уборщик")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Уборщик")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    await member.remove_roles(mutedRole)
    await ctx.respond(f"Мьют успешно снят с участника {member.mention}!")

@mute.error # Отсутствие прав для мута
async def permserror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ctx.respond('Прости, но у тебя нет прав для выполнения данной команды...')

# @bot.event
# async def on_ready():
#    print(f'Client ready as {bot.user}')

@bot.slash_command(description="Отправляет пинг бота.")
async def ping(ctx):
    await ctx.respond(f"Понг! Пинг бота - {bot.latency} секунд.")

keep_alive()
bot.run(token)
