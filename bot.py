import discord
from discord.ext import commands
import os
from discord.utils import get
import discord.utils
import asyncio
import aiohttp
import datetime
import time
import random

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = True

bot = commands.Bot(command_prefix='^', intents=intents)

@bot.event
async def on_ready():
  print(f"{bot.user} says:\nHello")


@bot.command()
@commands.has_permissions(administrator=True)
async def howTO(ctx):
  await ctx.message.delete()
  embed = discord.Embed(title='Ticketing System',
                        description='How to use the ticketing system.', colour=discord.Colour.dark_blue())
  embed.add_field(name='Creating a ticket',
                  value='To create a ticket just use the command ^generate and a new channel will be opened for you', inline=True)
  embed.add_field(name='Waiting after Opening a ticket',
                  value='All users who open a ticket must wait until some staff comes to their help', inline=True)
  embed.add_field(name='Closing a Ticket',
                  value='To close a ticket just type the message closeTicket in the new ticket channel created for you', inline=True)
  embed.set_image(url=ctx.guild.icon_url)
  embed.set_author(name='CrackedSkull')
  await ctx.send(embed=embed)


@bot.command(brief='This command generates a new ticket for the user!', aliases=['ticket'])
async def generate(ctx):
    await ctx.message.delete()
    warn = await ctx.send("Alright your ticket will be created")
    time.sleep(4)
    await warn.delete()
    author = ctx.author
    guild = ctx.message.guild
    client = bot.user
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True),
        client: discord.PermissionOverwrite(
            read_messages=True, manage_channels=True)
    }
    nameCAT = 'TICKET'
    category = discord.utils.get(ctx.guild.categories, name=nameCAT)
    TextChannel = await guild.create_text_channel(f'{ctx.author}', overwrites=overwrites, reason='Ticketing', category=category)
    await TextChannel.send(f'{ctx.author.mention}, Welcome, Type down your problem and until then i will get some support staff to answer your query. Just use the ^close command to close ticket. THANK YOU FOR YOUR COORDINATION.')
    def check(m):
        return m.content == "^close" and m.channel == TextChannel
    guild = ctx.message.guild
    msg = await bot.wait_for('message', check=check)
    await TextChannel.send("Ok so your ticket will be deleted")
    await ctx.TextChannel.set_permission(ctx.author, read_messages=True)


@bot.command(brief='This command can delete bulk messages!')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount)

@bot.command(aliases=['transcript', 'copy'])
@commands.has_permissions(administrator=True)
async def history(ctx, limit: int = 100):
    channel = ctx.message.channel
    messages = await ctx.channel.history(limit=limit).flatten()
    with open(f"{channel}_messages.txt", "a+", encoding="utf-8") as f:
        print(
            f"\nTranscript Saved by - {ctx.author.display_name}.\n\n", file=f)
        for message in messages:
            embed = ""
            if len(message.embeds) != 0:
                embed = message.embeds[0].description
                print(f"{message.author.name} - {embed}", file=f)
            print(f"{message.author.name} - {message.content}", file=f)
    await ctx.message.add_reaction("✅")
    await ctx.send(f"{ctx.author.mention}, Transcript saved.")
    history = discord.File(fp=f'{channel}_messages.txt', filename=None)
    await ctx.send(file=history)



bot.run(os.environ['DISCORD_TOKEN'])
