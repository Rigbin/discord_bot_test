import asyncio
import discord
import os
from dotenv import load_dotenv

client = discord.Client()

async def dm_on_message(message):
    print(f"dm from {message.author.display_name}")
    print(message.content)


@client.event
async def on_ready():
    print(f'logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        dm = await message.author.create_dm()
        dmessage = await dm.send(f'Hello {message.author.display_name}!\nWelche Klasse spielst du?')

        wow_classes_emojis = [":Warrior:839571089474322503", ":Rouge:839571089726504981", ":Hunter:839571088987521038"]

        for react in wow_classes_emojis:
            await dmessage.add_reaction(react)

        def check_react(reaction, user):
            if reaction.message.id != dm.id:
                return False
            if user != message.author:
                return False
            if str(reaction.emoji) not in wow_classes_emojis:
                return False
            return True

        try:
            # https://stackoverflow.com/questions/63837615/multiple-choice-reaction-python-discord-py
            # it looks like he uses an adiitional library (discord.ext) ?!, `client` is wrong at this place!
            res, user = await client.wait_for('reaction_add', check=check_react)
        except asyncio.TimoutError:
            return await dmessage.clear_reactions()

        if user != message.author:
            return
        elif ':Warrior:' in str(res.emoji):
            print(f'{message.author.display_name} is Warrior')
            await dm.send('Hello Warrior')
        elif ':Rouge:' in str(res.emoji):
            print(f'{message.author.display_name} is Rouge')
            await dm.send('Hello Rouge') 
        elif ':Hunter:' in str(res.emoji):
            print(f'{message.author.display_name} is Hunter')
            await dm.send('Hello Hunter')


    if message.content in ['Krieger', 'Magier', 'Schurke']:
        dm = await message.author.create_dm()
        await dm.send(f'Du bist also ein {message.content}')

        

load_dotenv()

print(os.getenv('TOKEN'))
client.run(os.getenv('TOKEN'))
