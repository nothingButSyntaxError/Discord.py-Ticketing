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


@bot.command(aliases=['tickets'])
async def ticket(ctx):
    guild = ctx.message.guild
    admin_role = get(guild.roles, name="Admin")
    bot_self = bot.user
    author = ctx.author
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        admin_role: discord.PermissionOverwrite(read_messages=True),
        bot_self: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
        author: discord.PermissionOverwrite(read_messages=True)
    }
    confirmation = await ctx.send(f"Hey, {ctx.author.mention} Please react to this message with the below emoji within 60 seconds to open a ticket.")
    await confirmation.add_reaction(emoji='✅')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '✅'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        guild = ctx.message.guild
        TicketChannel = await guild.create_text_channel(f'{ctx.author}', overwrites=overwrites)
        await TicketChannel.send(f"Hey, {ctx.author.mention}, you have opened a ticket so please wait until I get some support staff and until then please write your complaint down. Use the command ^transcript for a transcript and ^close to close the ticket.")
        def check2(m):
            m.content == '^transcript' and m.channel == TicketChannel
        msg = await bot.wait_for('message', check=check2)
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
        def check3(m):
            m.content == '^close' and m.channel == TicketChannel
        msg2 = await bot.wait_for('message', check=check3)
        await TicketChannel.send("Ok deleting your ticket in 5 seconds")
        await TicketChannel.delete()
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention}, You didnt react on time to open your ticket successfully.")


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
    

@bot.command(aliases=['del_chan'])
@commands.has_permissions(administrator=True)
async def shh(ctx):
    Channel = ctx.message.channel
    await Channel.delete()



bot.run(os.environ['DISCORD_TOKEN'])
