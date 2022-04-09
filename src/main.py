import asyncio, discord, time
from discord import Embed
from discord.ext import commands
from tksave import *
from status import *
from user import *
from game import *

'''
봇 정상적으로 작동되면 호출
'''
@bot.event
async def on_ready():
    print("I have logged in as {0.user}\n".format(bot))

# =============================== User ===============================

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
        embed = discord.Embed(title = "빙글빙글 돌아가는 맷돌~", description = '이미가입완.', color = discord.Color.blue())
        embed.set_thumbnail(url = url2)
        await ctx.send(embed = embed)

    # 회원 가입의 경우
    else:
        embed = discord.Embed(title = "회원 가입 완료!", description = '커다란 자갈돌은 짱돌~', color = discord.Color.blue())
        embed.set_thumbnail(url = url1)
        signUp(ctx.author.name, ctx.author.id)
        await ctx.send(embed = embed)

'''
유저 본인 정보 열람
@param ctx 그냥 context인데 이걸로 봇이 답장 보냄
'''
@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    # 만약에 가입이 되어 있을 경우
    if userExistance:
        level, money, loss = userInfo(userRow) # 해당하는 유저 찾아서 행 가지고 옴
        embed = discord.Embed(title = "쉿! 🤫 정보 열람 중...", description = "보여 드렸습니다~", color = discord.Color.dark_blue())
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "지갑", value = money)
        embed.add_field(name = "도박... 더 하시게요?", value = loss, inline = False)

        await ctx.send(embed = embed)

    # 아직 가입하지 않았을 경우
    else:
        embed = discord.Embed(title = "아원튜베이베~", description = '어쩔회원가입~', color = discord.Color.dark_blue())
        embed.set_thumbnail(url = url3)
        await ctx.send(embed = embed)    

# =============================== Game ===============================

'''
가위바위보 게임 (코드가 너무 더럽습니다...)
@param ctx 그냥 context인데 이걸로 봇이 답장 보냄
@param rsp 유저 가위바위보 패
@param money 도박에 배팅할 돈
@param mul 몇 배 배팅할 건지
'''
@bot.command()
async def 가위바위보(ctx, rsp, money, mul):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    botRSP = RSP()
    result = ""
    betting = 0

    # else문에 예외 상황 출력문 있으니 알잘딱 봅시다
    # 이건 무슨 함수지? 이런 건 다 user.py에 있습니다
    if userExistance:
        u_money = getMoney(ctx.author.name, userRow)
        if int(money) >= 10:
            if int(mul) == 2 or int(mul) == 3 or int(mul) == 5:
                if u_money >= int(money):
                    if rsp == "가위":
                        if botRSP == "가위":
                            result = "어쩌면... 운명일지도"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, 0)

                        elif botRSP == "바위":
                            result = "도박 접고 팡푸나 하시죠?"
                            betting = int(mul) * int(money)
                            
                            modifyMoney(ctx.author.name, userRow, -int(betting))
                            moneyLoss(ctx.author.name, userRow, int(betting))
                        
                        elif botRSP == "보":
                            result = "쫌... 치시네요?"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, int(betting))

                        embed = discord.Embed(title = "✌가위바위보 결과✌", description = result, color = discord.Color.dark_gray())
                        embed.add_field(name = "봇", value = botRSP)
                        embed.add_field(name = ctx.author.name, value = rsp)
                        embed.add_field(name = "도박에 걸려 있던 돈 💵", value = betting, inline = False)
                        embed.add_field(name = "현재 자산 💰", value = getMoney(ctx.author.name, userRow))

                        await ctx.send(embed = embed)
        
                    elif rsp == "바위":
                        if botRSP == "가위":
                            result = "쫌... 치시네요?"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, int(betting))

                        elif botRSP == "바위":
                            result = "어쩌면... 운명일지도"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, 0)
                        
                        elif botRSP == "보":
                            result = "도박 접고 팡푸나 하시죠?"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, -int(betting))
                            moneyLoss(ctx.author.name, userRow, int(betting))

                        embed = discord.Embed(title = "✌가위바위보 결과✌", description = result, color = discord.Color.dark_gray())
                        embed.add_field(name = "봇", value = botRSP)
                        embed.add_field(name = ctx.author.name, value = rsp)
                        embed.add_field(name = "도박에 걸려 있던 돈 💵", value = betting, inline = False)
                        embed.add_field(name = "현재 자산 💰", value = getMoney(ctx.author.name, userRow))

                        await ctx.send(embed = embed)
                    
                    elif rsp == "보":
                        if botRSP == "가위":
                            result = "도박 접고 팡푸나 하시죠?"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, -int(betting))
                            moneyLoss(ctx.author.name, userRow, int(betting))

                        elif botRSP == "바위":
                            result = "쫌... 치시네요?"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, int(betting))
                        
                        elif botRSP == "보":
                            result = "어쩌면... 운명일지도"
                            betting = int(mul) * int(money)

                            modifyMoney(ctx.author.name, userRow, 0)
                        
                        embed = discord.Embed(title = "✌가위바위보 결과✌", description = result, color = discord.Color.dark_gray())
                        embed.add_field(name = "봇", value = botRSP)
                        embed.add_field(name = ctx.author.name, value = rsp)
                        embed.add_field(name = "도박에 걸려 있던 돈 💵", value = betting, inline = False)
                        embed.add_field(name = "현재 자산 💰", value = getMoney(ctx.author.name, userRow))

                        await ctx.send(embed = embed)
                    
                    else:
                        await ctx.send("가위, 바위, 보만 입력 가능합니땅.")
                else:
                    embed = discord.Embed(title = "돈이 없땅....", description = '언제이렇게됐지....', color = discord.Color.dark_blue())
                    embed.set_thumbnail(url = url4)
                    await ctx.send(embed = embed)
            else:
                await ctx.send("배팅은 2, 3, 5배만 가능합니땅.")
        else:
            await ctx.send("10원 이상 배팅 가능합니땅.")

    else:
        embed = discord.Embed(title = "아원튜베이베~", description = '어쩔회원가입~', color = discord.Color.dark_blue())
        embed.set_thumbnail(url = url3)
        await ctx.send(embed = embed) 

bot.run(Token)