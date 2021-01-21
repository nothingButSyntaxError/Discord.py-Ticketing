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

bot = commands.Bot(command_prefix='^')

@bot.event
async def on_ready():
  print(f"{bot.user} says:\nHello")


@bot.event
async def on_guild_join(ctx, self):
  await ctx.guild.create_category(TICKET)


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
  async with ctx.typing():
    await ctx.message.delete()
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

    while True:
        def check(m):
            return m.content == "^close" and m.channel == TextChannel
        guild = ctx.message.guild
        msg = await bot.wait_for('message', check=check)
        await TextChannel.send("Alright deleting your ticket in 5 seconds......")
        time.sleep(5)
        await TextChannel.delete()


@bot.command(brief='This command can delete bulk messages!')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount)



bot.run(os.environ['DISCORD_TOKEN'])
