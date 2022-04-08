import discord, asyncio, random, os, sys
from discord.ext import commands
from tksave import Token

game = discord.Game("맨땅에 헤딩하며 개발")

bot = commands.Bot(command_prefix = "!", status = discord.Status.online, activity = game)