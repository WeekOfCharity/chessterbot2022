# ChessterBot created by Bina and Marlin for the Week of Charity 2022
# Updated for the Week of Charity 2023
#
# ChessterBot v.23.1.0

from multiprocessing import AuthenticationError
from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import *
import time
import math
import asyncio
import argparse
import random
import os

CHANNEL_LIST = [
    'nislregen',
    'deraltan',
    'gumlong',
    'grandtriskel',
    'EpicEugen1',
    'ennieways',
    'sir_nightmare94',
    'BinaKleinerAls3',
    'lisanougat',
    'KurisuVanEdge',
    'emtes',
    'badingoregrill',
    'miragaia_anco',
    'Placedelynn',
    'shinjis_world',
    'piatralisch'
]

YEAR = "2023"

MSG_FREQ = 1800 # In Seconds

# https://www.epochconverter.com/ -- Saturday, September 9, 2023 3:00:00 PM GMT+02:00
START_TIMESTAMP = datetime.fromtimestamp(1694264400)

WOC_START_JUST_NOW_TEXT = "Die Week of Charity hat gerade begonnen!"
WOC_START_IN_FUTURE_TEXT = f"Die Week of Charity {YEAR} started bald!"
WOC_END_TEXT = "Die Week of Charity ist vorbei! Bis zum nächsten Mal!"

ENG_WOC_START_JUST_NOW_TEXT = "The Week of Charity just started!"
ENG_WOC_START_IN_FUTURE_TEXT = f"The Week of Charity {YEAR} starts soon!"
ENG_WOC_END_TEXT = "The Week of Charity is over! See you next time!"

# Command texts
HELP_TEXT = "Folgende commands sind verfügbar: !website, !faq, !programm, !charity, !donate, !goals, !bidwar, !uptime, !shop, !youtube, !twitter, !tiktok, !instagram, !mastodon, !musik --- Add '_en' for english commands."
WEBSITE_TEXT = "Unsere Website: https://weekofcharity.de/ 🐄"
FAQ_TEXT = "Wichtige Fragen und Antworten in unserem FAQ: https://weekofcharity.de/#faq 🦉"
SCHEDULE_TEXT = "Hier findet ihr den Zeitplan des Events: https://weekofcharity.de/streams 🐓"
CHARITY_TEXT = "Hier findet ihr Informationen zur Charity: https://weekofcharity.de/projekte 🐱"
DONATE_TEXT = "Hier könnt ihr donaten: https://www.betterplace.org/de/fundraising-events/45057-week-of-charity-2023 🐶"
GOALS_TEXT = "Hier findet ihr alle Spendenziele: https://weekofcharity.de/#spenden 🐝"
BIDWAR_TEXT = "Entscheidet mit euren Spenden, über welches Tier Jesko ein Referat hält: https://weekofcharity.de/#bidwar 🐰"
SHOP_TEXT = "Wenn ihr Interesse an Merch habt, schaut hier rein: https://www.shirtee.com/de/store/weekofcharity/ 🦝"
YOUTUBE_TEXT = "Unser YouTube-Kanal für die Aufzeichnungen: https://www.youtube.com/@weekofcharity8094 🦔"
TWITTER_TEXT = "Hier gibt es die neusten Tweets: https://twitter.com/WeekOfCharity 🐦"
TIKTOK_TEXT = "Folgt uns auf TikTok für lustige Clips: https://www.tiktok.com/@weekofcharity 🐒"
INSTAGRAM_TEXT = "Folgt uns auf Instagram: https://www.instagram.com/weekofcharity/ 🦚"
MASTODON_TEXT = "Hier gibt es die neusten Tröts: https://tech.lgbt/@weekofcharity 🐘"
MUSIK_TEXT = "Die Musik wurde von amy und mioh gemacht: https://kleeder.bandcamp.com/album/week-of-charity-2022-soundtrack/ 🦜"

# Command texts [ENG]
ENG_HELP_TEXT = "The following commands are available: !website_en, !faq_en, !programm_en, !charity_en, !donate_en, !goals_en, !bidwar_en, !uptime_en, !shop_en, !youtube_en, !twitter_en, !tiktok_en, !instagram_en, !mastodon_en, !musik_en"
ENG_WEBSITE_TEXT = "Our website: https://weekofcharity.de/ 🐄"
ENG_FAQ_TEXT = "Frequently asked questions: https://weekofcharity.de/#faq 🦉"
ENG_SCHEDULE_TEXT = "Here you can find the schedule for our event: https://weekofcharity.de/streams 🐓"
ENG_CHARITY_TEXT = "Here you can find information about the charity we support: https://weekofcharity.de/projekte 🐱"
ENG_DONATE_TEXT = "Donate here: https://www.betterplace.org/de/fundraising-events/45057-week-of-charity-2023 🐶"
ENG_GOALS_TEXT = "Here you can find our donation goals: https://weekofcharity.de/#spenden 🐝"
ENG_BIDWAR_TEXT = "Decide with your donations which animal Jesko will give a presentation about: https://weekofcharity.de/#bidwar 🐰"
ENG_SHOP_TEXT = "Want some merch? Check out our shop: https://www.shirtee.com/de/store/weekofcharity/ 🦝"
ENG_YOUTUBE_TEXT = "Our YouTube channel for VODs: https://www.youtube.com/@weekofcharity8094 🦔"
ENG_TWITTER_TEXT = "Here you can find our latest tweets: https://twitter.com/WeekOfCharity 🐦"
ENG_TIKTOK_TEXT = "Follow us on TikTok for funny clips: https://www.tiktok.com/@weekofcharity 🐒"
ENG_INSTAGRAM_TEXT = "Follow us on Instagram: https://www.instagram.com/weekofcharity/ 🦚"
ENG_MASTODON_TEXT = "Here you can find our latest toots: https://tech.lgbt/@weekofcharity 🐘"
ENG_MUSIK_TEXT = "The music was made by amy and mioh: https://kleeder.bandcamp.com/album/week-of-charity-2022-soundtrack/ 🦜"

# Other texts
GERMAN_HELLO_TEXT = "Hallo, ich bin ChessterBot! Mit '!help' kannst du dir alle verfügbaren Commands anzeigen lassen. 🐾"
AUSTRIA_HELLO_TEXT = "Griaß di, i bin der ChessterBot! Mit '!help' konnst du dir olle verfügboren Commands anzeigen lossen. 🐾"
BAYRISCH_HELLO_TEXT = "Servus, i bin ChessterBot! Mit '!help' konnst du dir alle verfügbaren Commands ozoagn lassn. 🐾"
SCHWEIZER_HELLO_TEXT = "Grüezi, ig heisse ChessterBot! Mit '!help' chasch dir alli verfüegbare Commands azeige loh. 🐾"
LUXEMBURGISCH_HELLO_TEXT = "Moien, ech sinn den ChessterBot! Mat '!help' kanns du dir all disponible Commands weisen loossen. 🐾"
ENGLISH_HELLO_TEXT = "Hello, I'm ChessterBot! With '!help_en' you can check out all available commands. 🐾"

SCHALTSEKUNDEN_TEXT = "Wenn ihr Interesse an Schaltsekunden habt, schaut hier rein: https://de.wikipedia.org/wiki/Schaltsekunde 🐾"
ENG_SCHALTSEKUNDEN_TEXT = "Interested in Schaltsekunden? Check this out: https://de.wikipedia.org/wiki/Schaltsekunde 🐾"

SCHEDULED_MESSAGES = [WEBSITE_TEXT, SCHEDULE_TEXT, DONATE_TEXT, SHOP_TEXT]


def woc_format_time(td):
    if td.days == 0 and td.seconds < 10:
        return WOC_START_JUST_NOW_TEXT
    
    if td.days < 0:
        return WOC_START_IN_FUTURE_TEXT

    if td.days > 8:
        return WOC_END_TEXT

    seconds = td.seconds % 60
    minutes = math.floor(td.seconds / 60) % 60
    hours = math.floor(td.seconds / 3600)
    days = td.days

    output = "Die Week of Charity läuft bereits seit "

    if days > 1:
        output += str(days) + " Tagen, "
    elif days == 1:
        output += str(days) + " Tag, "

    if hours > 1:
        output += str(hours) + " Stunden, "
    elif hours == 1:
        output += str(hours) + " Stunde, "

    if minutes > 1:
        output += str(minutes) + " Minuten, "
    elif minutes == 1:
        output += str(minutes) + " Minute, "

    if seconds > 1:
        output += str(seconds) + " Sekunden, "
    elif seconds == 1:
        output += str(seconds) + " Sekunde, "

    output = output[:-2]
    output += "!"

    output = " und".join(output.rsplit(",", 1))

    return output

def woc_format_time_en(td):
    if td.days == 0 and td.seconds < 10:
        return ENG_WOC_START_JUST_NOW_TEXT
    
    if td.days < 0:
        return ENG_WOC_START_IN_FUTURE_TEXT

    if td.days > 8:
        return ENG_WOC_END_TEXT

    seconds = td.seconds % 60
    minutes = math.floor(td.seconds / 60) % 60
    hours = math.floor(td.seconds / 3600)
    days = td.days

    output = "The Week of Charity has been running for "

    if days > 1:
        output += str(days) + " days, "
    elif days == 1:
        output += str(days) + " day, "

    if hours > 1:
        output += str(hours) + " hours, "
    elif hours == 1:
        output += str(hours) + " hour, "

    if minutes > 1:
        output += str(minutes) + " minutes, "
    elif minutes == 1:
        output += str(minutes) + " minute, "

    if seconds > 1:
        output += str(seconds) + " seconds, "
    elif seconds == 1:
        output += str(seconds) + " second, "

    output = output[:-2]
    output += "!"

    output = " and".join(output.rsplit(",", 1))

    return output

def command_language(ctx):
    if ctx.message.content.find('_en') >= 0:
        return "en"
    return "de"

class Bot(commands.Bot):

    def __init__(self, api_token, hello_msg):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.api_token = api_token
        self.hello_msg = hello_msg
        super().__init__(token=api_token, prefix='!', initial_channels=CHANNEL_LIST)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        if self.hello_msg:
            self.hello_msg == False
            # Send a hello message to every channel
            for c in CHANNEL_LIST:
                channel = self.get_channel(c)
                await channel.send(GERMAN_HELLO_TEXT)
                print(f"Sent hello message @ ({c})")

        # Random scheduled messages
        while True:
            # Calculate time until next scheduled message.
            s = MSG_FREQ - time.time() % MSG_FREQ
            await asyncio.sleep(s)
            
            # Get a list of all streams that are currently live.
            fetch_streams_task = asyncio.create_task(self.fetch_streams(user_logins=CHANNEL_LIST))
            await fetch_streams_task
            streams = fetch_streams_task.result()

            # Choose random message
            random_message = random.choice(SCHEDULED_MESSAGES)
            
            # Send a message to all live channels
            for s in streams:
                if s.type == "live":
                    channel = self.get_channel(s.user.name)
                    await channel.send(random_message)
                    print(f"Sent scheduled message to live channel {s.user.name}")

    async def event_message(self, msg):
        if msg.echo:
            print(f"[ChessterBot] @ ({msg.channel.name}): '{msg.content}'")
            return
        print(f"[{msg.author.name}] @ ({msg.channel.name}): '{msg.content}'")
        await self.handle_commands(msg)
    
    ####################################

    @commands.command(aliases=["uptime_en"])
    async def uptime(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(f"{woc_format_time(datetime.now() - START_TIMESTAMP)} 🦊")
        elif language == "en":
            await ctx.send(f"{woc_format_time_en(datetime.now() - START_TIMESTAMP)} 🦊")

    @commands.command(aliases=["commands", "help_en"])
    async def help(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(HELP_TEXT)
        elif language == "en":
            await ctx.send(ENG_HELP_TEXT)
        

    ####################################

    # Basic chat commands
    @commands.command(aliases=["faq_en"])
    async def faq(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(FAQ_TEXT)
        elif language == "en":
            await ctx.send(ENG_FAQ_TEXT)

    @commands.command(aliases=["merch", "shop_en"])
    async def shop(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(SHOP_TEXT)
        elif language == "en":
            await ctx.send(ENG_SHOP_TEXT)

    @commands.command(aliases=["charity_en"])
    async def charity(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(CHARITY_TEXT)
        elif language == "en":
            await ctx.send(ENG_CHARITY_TEXT)

    @commands.command(aliases=["programm", "program", "zeitplan", "programm_en", "schedule_en", "program_en"])
    async def schedule(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(SCHEDULE_TEXT)
        elif language == "en":
            await ctx.send(ENG_SCHEDULE_TEXT)

    @commands.command(aliases=["twitter_en"])
    async def twitter(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(TWITTER_TEXT)
        elif language == "en":
            await ctx.send(ENG_TWITTER_TEXT)

    @commands.command(aliases=["donations", "donation", "spenden", "spende", "donate_en"])
    async def donate(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(DONATE_TEXT)
        elif language == "en":
            await ctx.send(ENG_DONATE_TEXT)

    @commands.command(aliases=["yt", "youtube_en"])
    async def youtube(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(YOUTUBE_TEXT)
        elif language == "en":
            await ctx.send(ENG_YOUTUBE_TEXT)

    @commands.command(aliases=["tiktok_en"])
    async def tiktok(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(TIKTOK_TEXT)
        elif language == "en":
            await ctx.send(ENG_TIKTOK_TEXT)
    
    @commands.command(aliases=["insta", "instagram_en", "insta_en"])
    async def instagram(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(INSTAGRAM_TEXT)
        elif language == "en":
            await ctx.send(ENG_INSTAGRAM_TEXT)
    
    @commands.command(aliases=["mastodon_en"])
    async def mastodon(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(MASTODON_TEXT)
        elif language == "en":
            await ctx.send(ENG_MASTODON_TEXT)

    @commands.command(aliases=["donationgoals", "goal", "spendenziele", "spendenziel", "ziele", "goals_en", "donationgoals_en"])
    async def goals(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(GOALS_TEXT)
        elif language == "en":
            await ctx.send(ENG_GOALS_TEXT)

    @commands.command(aliases=["abstimmung", "bidwar_en"])
    async def bidwar(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(BIDWAR_TEXT)
        elif language == "en":
            await ctx.send(ENG_BIDWAR_TEXT)

    @commands.command(aliases=["webseite", "seite", "site", "about", "info", "woc", "website_en", "info_en", "about_en", "site_en", "woc_en"])
    async def website(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(WEBSITE_TEXT)
        elif language == "en":
            await ctx.send(ENG_WEBSITE_TEXT)
    
    @commands.command(aliases=["musik", "56", "musik_en", "music_en"])
    async def music(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(MUSIK_TEXT)
        elif language == "en":
            await ctx.send(ENG_MUSIK_TEXT)

    @commands.command()
    async def hallo(self, ctx: commands.Context):
        await ctx.send(GERMAN_HELLO_TEXT)

    @commands.command()
    async def servus(self, ctx: commands.Context):
        await ctx.send(BAYRISCH_HELLO_TEXT)
    
    @commands.command()
    async def moien(self, ctx: commands.Context):
        await ctx.send(LUXEMBURGISCH_HELLO_TEXT)
    
    @commands.command(aliases=["griaßdi", "grüßgott"])
    async def servas(self, ctx: commands.Context):
        await ctx.send(AUSTRIA_HELLO_TEXT)
    
    @commands.command()
    async def grüezi(self, ctx: commands.Context):
        await ctx.send(SCHWEIZER_HELLO_TEXT)

    @commands.command(aliases=["hallo_en"])
    async def hello(self, ctx: commands.Context):
        await ctx.send(ENGLISH_HELLO_TEXT)

    @commands.command(aliases=["schaltminute", "schaltminuten", "schaltsekunde", "schaltsekunden_en", "schaltsekunde_en"])
    async def schaltsekunden(self, ctx: commands.Context):
        language = command_language(ctx)
        if language == "de":
            await ctx.send(SCHALTSEKUNDEN_TEXT)
        elif language == "en":
            await ctx.send(ENG_SCHALTSEKUNDEN_TEXT)

if __name__ == '__main__':
    print("Initialize ChessterBot...")
    parser = argparse.ArgumentParser(description=f'Week of Charity {YEAR} Twitch Chat Bot "ChessterBot".')
    parser.add_argument('-hello', '--hello_msg', default=False, action='store_true', help='Enable "Hello Message" in all chats the bot loggs into.')
    parser.add_argument('--token', type=str, default='', help='Token for Twitch API.')
    args = parser.parse_args()
    token = args.token

    load_dotenv()

    if len(token) < 1:
        print("Reading Access Token from .env file.")
        token = os.getenv('ACCESS_TOKEN')

    bot = Bot(token, args.hello_msg)
    print(f"Hello Test-Message in all channels enabled: {args.hello_msg}")
    print("Starting ChessterBot...")
    try:
        bot.run()
    except AuthenticationError:
        # This error handling doesnt work. Idk why, asyncio is weird.
        print("Invalid or no Access Token provided. Use --token to provide the Access Token or set up an .env in the root directory containing the ACCESS_TOKEN field to provide a valid token.")
        exit(1)
