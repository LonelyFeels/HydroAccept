import discord
from discord import client
from discord.ext import commands
import mysql.connector
import mysqlshopcredentials as credentials


class Shops(commands.Cog):
    def __init__(self,client):
        self.client = client


    #Commands
    @commands.command(aliases=['sreg'])
    async def storeregister(self, ctx, storename, location=None):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        owner = ctx.message.author

        # Rejection reasons: Store already exists under another owner OR the user is making another new store and they're already the owner of one
        mycursor.execute("SELECT * FROM Store_Directory WHERE StoreName=%s", (storename, ))
        alreadyexists = mycursor.fetchall()
        if len(alreadyexists) > 0:
            await ctx.send(f'{storename} with such name already exists in Stores database!')
        else:
            mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s", (owner.id,))
            data = mycursor.fetchall()
            if len(data)==0:
                mycursor.execute("INSERT INTO Store_Directory (UserID, Username, StoreName, Location, IsOwner) VALUES (%s, %s, %s, %s, 1)", (f"{owner.id}", f"{owner.display_name}", storename, location))
                db.commit()
                await ctx.send(f'{storename} successfully registered into Stores database.')
            else:
                mycursor.execute("SELECT IsOwner FROM Store_Directory WHERE UserID=%s", (owner.id,))
                isowner = mycursor.fetchall()
                if len(isowner) > 1:
                    await ctx.send('Your store is already registered in Stores database!')
                else:
                    if isowner[0][0] == 1:
                        await ctx.send('Your store is already registered in Stores database!')
                    else:
                        mycursor.execute("INSERT INTO Store_Directory (UserID, Username, StoreName, Location, IsOwner) VALUES (%s, %s, %s, %s, 1)", (f"{owner.id}", f"{owner.display_name}", storename, location))
                        db.commit()
                        await ctx.send(f'{storename} successfully registered into Stores database.')

    @storeregister.error
    async def storeregister_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('You have state your Store Name (and Location)!')

    # !storeedit [storename] [item] [quantity] [price] [description] or !sedit [storename] [item] [quantity] [price] [description]
    @commands.command(aliases=['sedit'])
    async def storeedit(self, ctx, storename, item, quantity:int, price:int, currency, description=None):
        db = mysql.connector.connect(
                host = credentials.host,
                port = credentials.port,
                user = credentials.user,
                password = credentials.password,
                database = credentials.database
        )
        mycursor = db.cursor()
        try:
            owner = ctx.message.author
            mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND StoreName=%s;", (owner.id, storename))
            data = mycursor.fetchall()
            dataempty = [] == data
            if len(data) == 0:
                await ctx.send('Either I could not find a store with that name or you are not a member of that store.')
            else:
                # Checks if Item is in Library of Minecraft Items
                mycursor.execute("SELECT EXISTS (SELECT Item FROM Item_List WHERE Item=%s)", (item,))
                data = mycursor.fetchall()
                print(mycursor.statement)
                print(data)
                if not data[0][0]:
                    # Assume the user did a misspell, and suggests an item from the list
                    mycursor.execute("SELECT Item FROM Item_List WHERE Item SOUNDS LIKE %s LIMIT 1", (item,))
                    data = mycursor.fetchall()
                    if len(data) != 0:
                        await ctx.send(f"Did you mean to update or add \"{str(data[0][0])}\" to your store? Try running this command: `!storeedit <store name> \"{str(data[0][0])}\" <quantity> <price>`")
                    else:
                        await ctx.send("I\'m not sure what you're trying to update or add. Try another search term.")
                else:
                    #try to update or add item to store
                    mycursor.execute("SELECT EXISTS (SELECT * FROM Item_Listings WHERE Item=%s AND StoreName=%s)", (item, storename))
                    itemexists = mycursor.fetchall()
                    if itemexists[0][0]:
                        mycursor.execute("UPDATE Item_Listings SET Quantity=%s, Price=%s, Currency=%s, Description=%s WHERE Item=%s AND StoreName=%s", (quantity, price, currency, description, item, storename))
                        db.commit()
                        updateresult = mycursor.rowcount
                        if updateresult > 0:
                            await ctx.send(f'The listing for {quantity}x {item}\'s price was successfully updated to {price} {currency}(s) for the {storename} Store.')
                        else:
                            await ctx.send("Something happened when trying to add an item from your store. Contact an Admin for help.")
                    else:
                        mycursor.execute("INSERT INTO Item_Listings (Item, StoreName, Quantity, Price, Currency, Description) VALUES (%s, %s, %s, %s, %s, %s)", (item, storename, quantity, price, currency, description))
                        db.commit()
                        addresult = mycursor.rowcount
                        if addresult > 0:
                            await ctx.send(f'A listing for {quantity}x {item} was successfully added at a price of {price} {currency}(s) for the {storename} Store.')
                        else:
                            await ctx.send("Something happened when trying to add an item from your store. Contact an Admin for help.")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            print(mycursor.statement)
            print(mycursor.fetchwarnings())

    @storeedit.error
    async def storeedit_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('You have to provide the Store Name, Item Name, Quantity, and Price (in Diamonds)!')

    # !storeitemlookup [item] or !itemlookup [item] or !slookup [item]
    @commands.command(aliases=['itemlookup','slookup'])
    async def storeitemlookup(self, ctx, item):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()

        # Checks if Item is in Library of Minecraft Items
        mycursor.execute("SELECT EXISTS (SELECT Item FROM Item_List WHERE Item=%s)", (item,))
        data = mycursor.fetchall()

        if not data[0][0]:
            # Assume the user did a misspell, and suggests an item from the list
            mycursor.execute("SELECT Item FROM Item_List WHERE Item SOUNDS LIKE %s LIMIT 1", (item,))
            data = mycursor.fetchall()
            if len(data) != 0:
                await ctx.send(f"Did you mean to look up \"{str(data[0][0])}\"? Try running this command: `!storeitemlookup \"{str(data[0][0])}\"`")
            else:
                await ctx.send("I\'m not sure what you're trying to lookup. Try another search term.")
        else:
            # Item exists in Library, display all listings for said item lookup
            mycursor.execute("SELECT EXISTS (SELECT StoreName, Quantity, Price, Currency, Description FROM Item_Listings WHERE Item=%s)", (item,))
            data = mycursor.fetchall()
            if data[0][0]:
                mycursor.execute("SELECT StoreName, Quantity, Price, Currency, Description FROM Item_Listings WHERE Item=%s", (item,))
                data = mycursor.fetchall()
                embeditemlookup = discord.Embed(
                    title = 'Store Item Lookup',
                    description = f'Showing all store listings for {item}.',
                    colour = discord.Colour.from_rgb(12,235,241)
                )
                for row in data:
                    embeditemlookup.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
                    embeditemlookup.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
                    if row[4] == None:
                        embeditemlookup.add_field(name=row[0], value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s)", inline=False)
                    else:
                        embeditemlookup.add_field(name=row[0], value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s) \n Description: {str(row[4])}", inline=False)
                await ctx.send(embed=embeditemlookup)
            else:
                await ctx.send(f"No one is currently selling any {str(item)}s.")

    @storeitemlookup.error
    async def storeitemlookup_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('Make sure to either have either a one word search term, or enclose your search term in quotations, like this:\n`!itemlookup "search term"`')
 
    # !storeremove [item] or !sr [item]
    @commands.command(aliases=['sr'])
    async def storeremove(self, ctx, storename, item):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        owner = ctx.message.author
        
        mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND StoreName=%s", (owner.id, storename))
        data = mycursor.fetchall()
        if len(data)==0:
            await ctx.send('Either I could not find a store with that name or you are not a member of that store.')
        else:
            # Checks if Item is in Library of Minecraft Items
            mycursor.execute("SELECT EXISTS (SELECT Item FROM Item_List WHERE Item=%s)", (item,))
            data = mycursor.fetchall()

            if not data[0][0]:
                # Assume the user did a misspell, and suggests an item from the list
                mycursor.execute("SELECT Item FROM Item_List WHERE Item SOUNDS LIKE %s LIMIT 1", (item,))
                data = mycursor.fetchall()
                if len(data) != 0:
                    await ctx.send(f"Did you mean to remove \"{str(data[0][0])}\" from your store? Try running this command: `!storeremove \"{str(data[0][0])}\"`")
                else:
                    await ctx.send("I\'m not sure what you're trying to remove. Try another search term.")
            else:
                # Try to remove item from store
                mycursor.execute("SELECT EXISTS (SELECT * FROM Item_Listings WHERE Item=%s AND StoreName=%s)", (item, storename))
                data = mycursor.fetchall()
                if not data[0][0]:
                    await ctx.send(f"You do not have any {str(item)}s in your store.")
                else:
                    mycursor.execute("DELETE FROM Item_Listings WHERE Item=%s AND StoreName=%s", (item, storename))
                    db.commit()
                    deleteresult = mycursor.rowcount
                    if deleteresult > 0: 
                        await ctx.send(f"Successfully removed {str(item)} from {str(storename)} store.")
                    else:
                        await ctx.send("Something happened when trying to remove an item from your store. Contact an Admin for help.")
   
    @storeremove.error
    async def storeremove_error(self, storename, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await storename.send('Make sure to either have either a one word search term, or enclose your search term in quotations, like this:\n`!storeremove "shopname" "search term"`')
   
    # !storecategories or !categories or !cat
    @commands.command(aliases=['categories', 'cat'])
    async def storecategories(self, ctx):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()

        mycursor.execute("SELECT DISTINCT Category FROM Item_List")
        data = mycursor.fetchall()
        embedcategories = discord.Embed(
            title = 'Item Categories',
            colour = discord.Colour.from_rgb(12,235,241)
        )

        categorylist = ""
        for row in data:
            categorylist = categorylist + str(row[0]) + "\n"

        embedcategories.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedcategories.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedcategories.add_field(name="Showing all item categories for the Store Listings", value=categorylist, inline=False)
        await ctx.send(embed=embedcategories)

    # !categoriesitems [category] or !cati [category]
    @commands.command(aliases=['cati'])
    async def categoriesitems(self, ctx, category):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        
        # Checks if Item is in Library of Minecraft Items
        mycursor.execute("SELECT EXISTS (SELECT Category FROM Item_List WHERE Category=%s)", (category,))
        data = mycursor.fetchall()

        if not data[0][0]:
            # Assume the user did a misspell, and suggests an Category from the list
            mycursor.execute("SELECT Category FROM Item_List WHERE Category SOUNDS LIKE %s LIMIT 1", (category,))
            data = mycursor.fetchall()
            if len(data) != 0:
                await ctx.send(f"Did you mean to look up \"{str(data[0][0])}\"? Try running this command: `!cati \"{str(data[0][0])}\"`")
            else:
                await ctx.send("I\'m not sure what you're trying to lookup. Try another search term.")
        else:
            mycursor.execute("SELECT Item FROM Item_List WHERE Category=%s", (category,))
            data = mycursor.fetchall()

            embedcitems = discord.Embed(
                title = f'Items in the {str(category)} Category',
                colour = discord.Colour.from_rgb(12,235,241)
            )
            embedcitems.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
            embedcitems.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')

            i = 1
            section = 0
            nextstring = data[0][0] + "\n"
            while i <= len(data):
                currentstring = ""
                while len(currentstring) + len(nextstring) < 1024 and i<= len(data):
                    currentstring = currentstring + nextstring
                    if i < len(data):
                        nextstring = str(data[i][0]) + "\n"
                    i += 1
                section += 1
                embedcitems.add_field(name=f"{str(category)} {str(section)}", value=currentstring, inline=False)

            await ctx.send(embed=embedcitems)
    
    @categoriesitems.error
    async def categoriesitems_error(self, category, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await category.send('You have to state the Category you want to see Items in.')

    # !storeunregister or !sunreg
    @commands.command(aliases=['sunreg'])
    async def storeunregister(self, ctx):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()

        owner = ctx.message.author
        mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND IsOwner=1", (owner.id,))
        data = mycursor.fetchall()
        if len(data)==0:
            await ctx.send('Your store does not exist in Stores database!')
        else:
            storename = data[0][2]
            mycursor.execute("SELECT * FROM Item_Listings WHERE StoreName=%s", (storename,))
            itemcount = mycursor.fetchall()
            if len(itemcount)==0:
                mycursor.execute("DELETE FROM Store_Directory WHERE StoreName=%s", (storename,))
                db.commit()
                deleteshop = mycursor.rowcount
                if deleteshop > 0:
                    await ctx.send(f'Successfully unregistered store {storename}.')
                else:
                    await ctx.send('Something happened when trying to unregister your shop. Contact an Admin for help.')
            else:
                mycursor.execute("DELETE FROM Item_Listings WHERE StoreName=%s", (storename,))
                db.commit()
                deleteresult = mycursor.rowcount
                if deleteresult > 0: 
                    await ctx.send(f"Successfully removed all items from your store.")
                    mycursor.execute("DELETE FROM Store_Directory WHERE StoreName=%s", (storename,))
                    db.commit()
                    deleteshop = mycursor.rowcount
                    if deleteshop > 0:
                        await ctx.send(f'Successfully unregistered store {storename}.')
                    else:
                        await ctx.send('Something happened when trying to unregister your shop. Contact an Admin for help.')
                else:
                    await ctx.send("Something happened when trying to remove items from your store. Contact an Admin for help.")

    # !store
    @commands.command(aliases=['shop'])
    async def store(self, ctx, storereference):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()

        # To check if the user entered a user's tag, or a store name, we check size of string and beginning characters
        # 22 is the standard length of a member reference
        if len(storereference) == 22 and storereference[0:3] == "<@!":
            ownerid = storereference[3:21]
            mycursor.execute("SELECT EXISTS (SELECT * FROM Store_Directory WHERE UserID=%s AND IsOwner=1)", (ownerid,))
            data = mycursor.fetchall()
            if len(data) == 0:
                await ctx.send("I could not find a store that is owned by that player.")
            else:
                mycursor.execute("SELECT StoreName FROM Store_Directory WHERE UserID=%s AND IsOwner=1 LIMIT 1", (ownerid,))
                data = mycursor.fetchall()
                storename = data[0][0]
                # Store exists, display all listings for said item lookup
                mycursor.execute("SELECT EXISTS (SELECT Item, Quantity, Price, Currency, Description FROM Item_Listings WHERE StoreName=%s)", (storename,))
                data = mycursor.fetchall()
                if data[0][0]:
                    mycursor.execute("SELECT Item, Quantity, Price, Currency, Description FROM Item_Listings WHERE StoreName=%s", (storename))
                    data = mycursor.fetchall()
                    embedstoreup = discord.Embed(
                        title = 'Store Lookup',
                        description = f'Showing all listings for the {storename} store.',
                        colour = discord.Colour.from_rgb(12,235,241)
                    )
                    for row in data:
                        embedstoreup.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
                        embedstoreup.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
                        if row[4] == None:
                            embedstoreup.add_field(name=f"{str(row[0])}", value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s)", inline=False)
                        else:
                            embedstoreup.add_field(name=f"{str(row[0])}", value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s) \n Description: {str(row[4])}", inline=False)
                    await ctx.send(embed=embedstoreup)
                else:
                    await ctx.send(f"The {storename} store currently does not have any items for sale.")
        else:
            storename = storereference
            mycursor.execute("SELECT StoreName FROM Store_Directory WHERE StoreName=%s LIMIT 1", (storename,))
            data = mycursor.fetchall()
            storename = data[0][0]

            if data[0][0]:
                # Store exists, display all listings for said item lookup
                mycursor.execute("SELECT EXISTS (SELECT Item, Quantity, Price, Currency, Description FROM Item_Listings WHERE StoreName=%s)", (storename,))
                data = mycursor.fetchall()

                if data[0][0]:
                    mycursor.execute("SELECT Item, Quantity, Price, Currency, Description FROM Item_Listings WHERE StoreName=%s", (storename,))
                    data = mycursor.fetchall()
                    embedstoreup = discord.Embed(
                        title = 'Store Lookup',
                        description = f'Showing all listings for the {storename} store.',
                        colour = discord.Colour.from_rgb(12,235,241)
                    )
                    for row in data:
                        embedstoreup.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
                        embedstoreup.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
                        if row[4] == None:
                            embedstoreup.add_field(name=f"{str(row[0])}", value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s)", inline=False)
                        else:
                            embedstoreup.add_field(name=f"{str(row[0])}", value=f"Quantity: {str(row[1])} \n Price: {str(row[2])} {str(row[3])}(s) \n Description: {str(row[4])}", inline=False)
                    await ctx.send(embed=embedstoreup)
                else:
                    await ctx.send(f"The {storename} store currently does not have any items for sale.")
            else:
                await ctx.send("There is no store under that name. Try again.")

    @commands.command(aliases=['storeaddm'])
    async def storeaddmember(self, ctx, member: discord.Member):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        owner = ctx.message.author

        mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND IsOwner=1", (owner.id,))
        data = mycursor.fetchall()
        if len(data) != 0:
            storename = data[0][2]
            location = data[0][3]
            mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND StoreName=%s AND IsOwner=0", (member.id, storename))
            ismember = mycursor.fetchall()
            if len(ismember) == 0:
                mycursor.execute("INSERT INTO Store_Directory (UserID, Username, StoreName, Location, IsOwner) VALUES (%s, %s, %s, %s, 0)", (member.id, member.display_name, storename, location))
                db.commit()
                await ctx.send(f'{member} successfully added to the {str(storename)} store.')
            else:
                await ctx.send(f'{member} is already member of {str(storename)} store!')
        else:
            await ctx.send('You currently don\'t own a store! Try registering one with `!storeregister [Store Name] [Location]`')

    @storeaddmember.error
    async def storeaddmember_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('You have to mention the member you want to add to your store!')

    @commands.command(aliases=['storeremm','storeremmember'])
    async def storeremovemember(self, ctx, member: discord.Member):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        owner = ctx.message.author

        mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND IsOwner=1", (owner.id,))
        data = mycursor.fetchall()
        if len(data) != 0:
            storename = data[0][2]
            mycursor.execute("DELETE FROM Store_Directory WHERE StoreName=%s AND UserID=%s AND IsOwner=0", (storename, member.id))
            db.commit()
            removeresult = mycursor.rowcount
            if removeresult > 0:
                await ctx.send(f'{member} successfully removed from the {str(storename)} store.')
            else:
                await ctx.send(f'{member} is not a member of your shop.')
        else:
            await ctx.send('You currently don\'t own a store! Try registering one with `!storeregister [Store Name] [Location]`')

    @storeremovemember.error
    async def storeremovemember_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('You have mention the member you want to remove from your store!')

    # !stores
    @commands.command(aliases=['shops'])
    async def stores(self, ctx):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()

        mycursor.execute("SELECT DISTINCT StoreName FROM Store_Directory")
        data = mycursor.fetchall()
        embedstores = discord.Embed(
            title = 'List of Stores',
            colour = discord.Colour.from_rgb(12,235,241)
        )

        storeslist = ""
        for row in data:
            storeslist = storeslist + str(row[0]) + "\n"

        if storeslist == "":
            storeslist = "There\'s no stores registered!"

        embedstores.set_footer(text=f'@ Hydro Vanilla SMP', icon_url='https://i.imgur.com/VkgebnW.png')
        embedstores.set_thumbnail(url='https://i.imgur.com/VkgebnW.png')
        embedstores.add_field(name="Showing all Stores for the Stores Category", value=storeslist, inline=False)

        await ctx.send(embed=embedstores)

    @commands.command(aliases=['sleave'])
    async def storeleave(self, ctx, storename):
        db = mysql.connector.connect(
            host = credentials.host,
            port = credentials.port,
            user = credentials.user,
            password = credentials.password,
            database = credentials.database
        )
        mycursor = db.cursor()
        member = ctx.message.author

        mycursor.execute("SELECT * FROM Store_Directory WHERE UserID=%s AND StoreName=%s AND IsOwner=1", (member.id, storename))
        data = mycursor.fetchall()
        if len(data) == 0:
            mycursor.execute("DELETE FROM Store_Directory WHERE StoreName=%s AND UserID=%s AND IsOwner=0", (storename, member.id))
            db.commit()
            removeresult = mycursor.rowcount
            if removeresult > 0:
                await ctx.send(f'Successfully left the {str(storename)} store.')
            else:
                await ctx.send('You are not a member of that store!')
        else:
            await ctx.send('You own that store! Try using `!sunreg` instead, if you want to delete the store.')

    @storeleave.error
    async def storeleave_error(self, username, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await username.send('You have mention the store you want to leave!')

        
def setup(client):
    client.add_cog(Shops(client))