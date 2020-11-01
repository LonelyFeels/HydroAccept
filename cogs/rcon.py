import discord
from discord.ext import commands
from minecraft import Server
import credentials


class RCON(commands.Cog):

    def __init__(self,client):
        self.client = client


    #Commands
    @commands.command()
    @commands.has_role('Staff')
    async def whitelist(self, ctx, player):
        ip = credentials.ip
        port = credentials.port
        password = credentials.password

        server = Server(ip, port, password, connect_on_send=True)
        print(await server.send(f'whitelist add {player}'))
        await ctx.send(f'Added {player} to the whitelist.')

        await server.close()

    @whitelist.error
    async def whitelist_error(self, player, error):
        if isinstance(error, commands.MissingRole):
            await player.send("You don't have the permissions to do that!")
        if isinstance(error, commands.MissingRequiredArgument):
            await player.send('You have to put member\'s IGN that you want to whitelist!')

    @commands.command()
    @commands.has_role('Staff')
    async def unwhitelist(self, ctx, player):
        ip = credentials.ip
        port = credentials.port
        password = credentials.password

        server = Server(ip, port, password, connect_on_send=True)
        print(await server.send(f'whitelist remove {player}'))
        await ctx.send(f'Removed {player} to the whitelist.')

        await server.close()
    
    @unwhitelist.error
    async def unwhitelist_error(self, player, error):
        if isinstance(error, commands.MissingRole):
            await player.send("You don't have the permissions to do that!")
        if isinstance(error, commands.MissingRequiredArgument):
            await player.send('You have to put member\'s IGN that you want to unwhitelist!')
    
    @commands.command()
    @commands.has_role('Staff')
    async def close(self, ctx):
        ip = credentials.ip
        port = credentials.port
        password = credentials.password

        server = Server(ip, port, password, connect_on_send=True)

        await server.close()

    @close.error
    async def close_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the permissions to do that!")


def setup(client):
    client.add_cog(RCON(client))