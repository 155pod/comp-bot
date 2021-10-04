import random
import discord.utils
from discord.ext import commands

random.seed()

def get_enqueue_response(bot: commands.Bot):

    def emoji(emoji_name):
        if bot is None:
            return emoji_name
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

def get_song_response(bot: commands.Bot, source):

    lower_title = source.title.lower()

    sclusie_responses = {
        "shoes" : [
            "Can you believe a SHOE made that?!"    
        ],
        "laundromat" : [
            "Come on man, I'm just trying to wash my shorts!"
        ],
        "baby" : [
            "Our little baby has done it again!"
        ]
    }

    normie_responses = [
        "Wow, that was like an early Modest Mouse demo.",
        "That was siiiiiiiick.",
        "Several people are typing...!!!",
        "That was untouchable perfect art.",
        "Damn okay. That was pretty vibey.",
        "That was just a lovely sadsack alt-country tune from my sweet babies.",
        "Wow the end just happened this song fucking rules holy shit.",
        "It’s so cool to listen to bands that keep getting older and evolving, particularly when no one else seems to care anymore.",
        "Here that was! And now I like it? Like truly I think this was the moment. Cool.",
        "That was something that half of us are fucking psyched for and the other half will just have to accept.",
        "The way this song moved from sorta-shoegaze to precocious pop rules, and it sets the table nicely for what is to come (more sick shit).",
        "This certainly has some of the previous charm, but the expanded sound gives it Kurt Vile-esque vibe that means it’ll surely be playing in laid-back roasteries that sell heather grey Alternative Apparel crewnecks, and Lord knows those people make the best coffee.",
        "This song would absolutely work on an early Big Shiny Tunes between Zuckerbaby and Limblifter tunes.",
        "How cool would it be if this was a song by Jesse Farrar.",
        "Mere months ago it would have sounded impossibly stupid, but this just sounds like normal music now.",
        "As someone who never stopped listening to uncool 90s music, I appreciate how much the gum I like is back in style these days.",
        "Coldplay is so sick. BTS is so sick. There’s probably some amazing choreo involved too. Fuck yeah. That rocked.",
        "There’s precious few things from my youth I haven’t already spelunked to death, and to add this beautiful nugget to my memory has been the treat of the week.",
        "Honestly this could be a Tragically Hip/Serial Joe collab.",
        "This beefy but emotive metalcore sounded like a faded black youth large hoodie that has an impossibly large, near-medieval hood.",
        "That's the kinda shit that makes you want to elbow a youth pastor.",
        "So weird that that was actually about god.",
        "This is fucking sick. When the harms hit I ascended.",
        "That was another one I think is basically perfect and it’s not even about being a punk businessman.",
        "Damn I bet Sam loved that chorus.",
        "I appreciated that the song made a point to counterbalance the glibness with an equally hooky reminder that they are simply shitting on exclusively cis men.",
        "That could just as easily have been a mosh call for a brutally corny deathcore band beloved by people who go to board game cafes.",
        "That was the kind of song that deserves to be everyone’s favourite, but it’s even better that it’s a secret cult classic.",
        "I want to party to that in a crowded bar with all my friends when this is all over.",
        "That was music you can only listen to at home alone with the door closed and a towel pushed up against the crack at the bottom. The real shit.",
        "Something about the spoken-word and chord progressions remind me of Envy, but then there’s so much Dragonforce, Andrew WK and, to keep things topical, modern Comeback Kid. What a delight.",
        "That was sick as all hell, made me want to mosh in the chippy.",
        "It’s starting to feel like that last one will never be handed the dumptruck full of money they deserve.",
        "That was the exact kind of music I wanted to write when I was 20, written by people much more talented than me at 20.",
        "That sounded Christian AF. Like the slightly more restrained cool-guy worship band that plays the young adult service.",
        "This could have been a standout on a Kacey Musgraves album, and instead its by a band with a name so dumb I am forced to admire it as a combination of naked pop ambition and stupid punk shit.",
        "That was a beautiful and vibey slowdance tune that hits in all the right ways.",
        "I’m happy to say that sounded extremely Christian.",
        "Holy shit that was incredible.",
        "Why does everyone here an enviably sick synth pop project? Why am I still just recording Dashbot Confessional covers?",
        "That was like if AI wrote a Sam jam!"
    ]

    for key, value in sclusie_responses.items():
        if key in lower_title:
            return random.choice(value)

    return random.choice(normie_responses)

if __name__ == "__main__":
    class TestSource:
        title = ""
        def __init__(self, title=""):
            self.title = title

    print(get_song_response(None, TestSource("Baby Tyler")))
    print(get_song_response(None, TestSource("ShoesRobinson")))
    print(get_song_response(None, TestSource()))

    print(get_enqueue_response(None))
    print(get_enqueue_response(None))
    print(get_enqueue_response(None))
