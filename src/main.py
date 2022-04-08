import asyncio, discord, time 
from discord import Embed
from discord.ext import commands
from tksave import *
from status import *
from user import *

'''
봇 정상적으로 작동되면 호출
'''
@bot.event
async def on_ready():
    print("I have logged in as {0.user}\n".format(bot))

'''
유저 회원 가입
@param ctx 그냥 context인데 이걸로 봇이 답장 보냄
'''
@bot.command()
async def 나도해볼래(ctx):
    # user 가입되어 있는지 찾기
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id) 

    # 만약에 가입이 되어 있을 경우
    if userExistance:
        embed = discord.Embed(title="빙글빙글 돌아가는 맷돌~", description='이미가입완.', color=discord.Color.blue())
        embed.set_thumbnail(url=url2)
        await ctx.send(embed = embed)
    # 회원 가입의 경우
    else:
        embed = discord.Embed(title="회원 가입 완료!", description='커다란 자갈돌은 짱돌~', color=discord.Color.blue())
        embed.set_thumbnail(url=url1)
        signUp(ctx.author.name, ctx.author.id)
        await ctx.send(embed = embed)
    
bot.run(Token)