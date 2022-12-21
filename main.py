import discord
import os
from discord.ext import commands, bridge
from webserver import keep_alive

token = os.environ.get("token")
intents = discord.Intents()
intents.message_content = True
bot = bridge.Bot(command_prefix=os.environ.get("prefix"), intents=intents)


@bot.event  # Запуск (инфо в консоли)
async def on_ready():
    print(f'{bot.user.name} запустился и готов к работе!')


@bot.bridge_command(description='Заставит кого угодно замолчать.')  # Мьют
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Уборщик")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Уборщик")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)
    await member.add_roles(mutedRole)
    await ctx.respond(f"Мьют успешно выдан участнику {member.mention}!")


@bot.bridge_command(
    description='Любому молчанию должен прийти конец, не так ли?')  # Размьют
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Уборщик")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Уборщик")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)
    await member.remove_roles(mutedRole)
    await ctx.respond(f"Мьют успешно снят с участника {member.mention}!")


@mute.error  # Отсутствие прав для мута
async def permserror(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        ctx.respond(
            'Прости, но у тебя нет прав для выполнения данной команды...')


class MyView(discord.ui.View): # UI-класс пинга
    @discord.ui.button(label="Получить задержку бота!", style=discord.ButtonStyle.primary, emoji="🏓")
    async def button_callback(self, button, interaction):
        await interaction.response.send_message(f"Задержка между получением запроса и выполнением команды - {bot.latency} секунд!") 

@bot.bridge_command(description="Отправляет пинг бота.") # Пинг
async def ping(ctx):
    await ctx.respond("Нажми на кнопку для получения пинга бота!", view=MyView())

@bot.bridge_command(description="Отправляет сумму двух чисел.")
async def add(ctx, a: int, b: int):
  await ctx.respond(a + b)

@bot.bridge_command(description="Отправляет разность двух чисел.")
async def subtract(ctx, a: int, b: int):
  await ctx.respond(a - b)

@bot.bridge_command(description="Отправляет произведение двух чисел.")
async def multiply(ctx, a: int, b: int):
  await ctx.respond(a + b)

@bot.bridge_command(description="Отправляет частное двух чисел.")
async def divide(ctx, a: int, b: int):
  await ctx.respond(a / b)

@bot.event # Отсутствие команды
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда набрана неправильно, или не существует. Проверьте в меню слэш-команд!")

keep_alive()
bot.run(token)
