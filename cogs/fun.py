import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import json
from datetime import datetime


class Fun(commands.Cog):

    def __init__(self,client):
        self.client = client


    #Commands
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                    'It is decidedly so.',
                    'Without a douubt.',
                    'Yes - definitely.',
                    'You may rely on it.',
                    'As I see it, yes',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good',
                    'Very doubtful.']
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        author = ctx.message.author
        author_icon = author.avatar_url
        embedhug = discord.Embed(
            colour = discord.Colour.from_rgb(12,235,241)
            )

        embedhug.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedhug.set_author(name=f'{author}', icon_url=f'{author_icon}')
        embedhug.set_image(url='https://i.imgur.com/kSWpxnG.gif')
        embedhug.add_field(name=f'@{member} I just hugged you in my thoughts :heart:', value='Hope you felt the squeeze! :teddy_bear:', inline=False)

        await ctx.send(embed=embedhug)

    @hug.error
    async def hug_error(self, member, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await member.send('You have to mention the Member you want to hug.')

    @commands.command()
    async def waifu(self, ctx):
        page = requests.get('http://randomwaifu.altervista.org')
        soup = bs(page.content, features='html.parser')
        url = str(soup.find_all(class_="center-fit")[0])[-18:][:15]
        name = str(soup.find_all(align="center")[0]).split(' from')[0][55:]
        channel = self.client.get_channel(859119453903781908)

        if ctx.channel.id == channel.id:
            embedwaifu = discord.Embed(
                title = f'{name}',
                url = f'http://randomwaifu.altervista.org/{url}',
                colour = discord.Colour.from_rgb(12,235,241)
            )

            embedwaifu.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
            embedwaifu.set_image(url=f'http://randomwaifu.altervista.org/{url}')
            embedwaifu.add_field(name='_ _', value='If the picutre doesn\'t load, that means it\'s too big.\nClick the name and it will open on your browser.', inline=False)

            await ctx.send(embed=embedwaifu)
        else:
            await ctx.send(f'You can only use this command in {channel.mention}.')

    @commands.command()
    async def dogfact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/dog")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/dog")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']

        embeddog = discord.Embed(
            title = 'Dog Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embeddog.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embeddog.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embeddog.set_image(url=f'{img}')
        embeddog.add_field(name='Woof woof 🐕', value=f'{fact}', inline=False)

        await ctx.send(embed=embeddog)

    @commands.command()
    async def catfact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/cat")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/cat")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']
        
        embedcat = discord.Embed(
            title = 'Cat Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embedcat.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedcat.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedcat.set_image(url=f'{img}')
        embedcat.add_field(name='Meow 🐈‍⬛', value=f'{fact}', inline=False)

        await ctx.send(embed=embedcat)

    @commands.command()
    async def pandafact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/panda")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/panda")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']
        
        embedpanda = discord.Embed(
            title = 'Panda Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embedpanda.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedpanda.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedpanda.set_image(url=f'{img}')
        embedpanda.add_field(name='squeak? 🐼', value=f'{fact}', inline=False)

        await ctx.send(embed=embedpanda)

    @commands.command()
    async def foxfact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/fox")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/fox")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']
        
        embedfox = discord.Embed(
            title = 'Fox Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embedfox.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedfox.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedfox.set_image(url=f'{img}')
        embedfox.add_field(name='What does the fox say? 🦊', value=f'{fact}', inline=False)

        await ctx.send(embed=embedfox)

    @commands.command()
    async def birdfact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/bird")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/birb")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']
        
        embedbird = discord.Embed(
            title = 'Bird Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embedbird.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedbird.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedbird.set_image(url=f'{img}')
        embedbird.add_field(name='Tweet 🐦', value=f'{fact}', inline=False)

        await ctx.send(embed=embedbird)

    @commands.command()
    async def koalafact(self, ctx):
        response = urllib.request.urlopen("https://some-random-api.ml/facts/koala")
        imgresponse = urllib.request.urlopen("https://some-random-api.ml/img/koala")
        data = json.load(response)
        imgdata = json.load(imgresponse)
        fact = data['fact']
        img = imgdata['link']
        
        embedkoala = discord.Embed(
            title = 'Koala Fact',
            colour = discord.Colour.from_rgb(12,235,241)
        )
        
        embedkoala.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedkoala.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedkoala.set_image(url=f'{img}')
        embedkoala.add_field(name='Tweet 🐨', value=f'{fact}', inline=False)

        await ctx.send(embed=embedkoala)

    @commands.command()
    async def christmas(self, ctx):
        #now = datetime.now()
        #christmas = datetime(2020, 12, 25)

        embedchristmas = discord.Embed(
            title = 'It\'s Beginning To Look A Lot Like Christmas',
            url='https://www.youtube.com/watch?v=QJ5DOWPGxwg',
            colour = discord.Colour.from_rgb(12,235,241)
        )

        embedchristmas.set_footer(text=f'Wishes from @ Hydro Vanilla SMP Staff', icon_url='https://i.imgur.com/VkgebnW.png')
        embedchristmas.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        #embedchristmas.add_field(name='Ho Ho Ho 🎅 Merry Christmas ☃️ And a Happy ❄️ New Year! 🌨️', value=f'Days left till Christmas: {(christmas.date()-now.date()).days}', inline=False)
        embedchristmas.add_field(name='Ho Ho Ho 🎅 Merry Christmas ☃️ And a Happy ❄️ New Year! 🌨️', value=f'*Christmas...*', inline=False)
        embedchristmas.add_field(name='_ _', value=f'gives us an opportunity\nto pause and reflect\non what *really matters*...', inline=False)
        embedchristmas.add_field(name='_ _', value=f'It\'s not\nwhat\'s under\nthe *Christmas tree* -\nbut who gathered\naround it.', inline=False)
        embedchristmas.add_field(name='_ _', value=f'May the *joys of today*\nwarm your heart,\nfill your home\n*and last a lifetime*.', inline=False)
        embedchristmas.add_field(name='_ _', value=f'*Have a very Merry Christmas* 🎅 🎁', inline=False)

        await ctx.send(embed=embedchristmas)

    @commands.command()
    async def newyear(self, ctx):
        embednewyear = discord.Embed(
            title = 'New Year 2021',
            url='https://www.youtube.com/watch?v=3Uo0JAUWijM',
            colour = discord.Colour.from_rgb(12,235,241)
        )

        embednewyear.set_footer(text=f'Wishes from @ Hydro Vanilla SMP Staff', icon_url='https://i.imgur.com/VkgebnW.png')
        embednewyear.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embednewyear.add_field(name='Happy New Year 2021! 🎉', value=f'*Life is too short* to wake up in the morning\nwith regrets.', inline=False)
        embednewyear.add_field(name='_ _', value=f'So, *love* the people who treat you right\nand *forget* about the ones who don\'t.', inline=False)
        embednewyear.add_field(name='_ _', value=f'And *believe*\nthat everything happens for a reason...\nif you have a chance - *take it*;\nif it changes your life - *let it*.', inline=False)
        embednewyear.add_field(name='_ _', value=f'Nobody said that it would be *easy*...\nThey just *promised*\nit would be *worth it*.', inline=False)
        embednewyear.add_field(name='_ _', value=f'We\'re wishing you *Peace*,\n*Love* and\n*Laughter*\nin the **New Year 2021** 🎉 🥂', inline=False)

        await ctx.send(embed=embednewyear)


def setup(client):
    client.add_cog(Fun(client))