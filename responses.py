import random
import discord.utils
from discord.ext import commands

random.seed()

def get_enqueue_response(bot: commands.Bot):

    def emoji(emoji_name):
        return str(discord.utils.get(bot.emojis, name=emoji_name))

    return random.choice([
        "Siiick!",
        "LetsFuckingGallop!",
        "Let's Go!",
        "Sick.",
        "oh shit.",
        ":sweat_drops:",
        emoji("LFG"),
        emoji("avrilpizza"),
        emoji("kravis"),
        emoji("saminthedark"),
        emoji("cigmark"),
        emoji("avsun"),
        emoji("podmagic2")
    ])


if __name__ == "__main__":
    print(get_enqueue_response())
