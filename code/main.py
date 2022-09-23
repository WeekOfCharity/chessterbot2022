# ChessterBot created by Bina and Marlin for the Week of Charity 2022

# TODO:
# - Automatisch reconnecten bei Verbindungsverlust (Vielleicht nicht nötig)

from twitchio.ext import commands
from datetime import *
import time
import math
import asyncio
import argparse
import random

ACCESS_TOKEN = "713jpa4s5jqa5inxf2zlxwlcpynj5r"
# CHANNEL_LIST = ['binakleinerals3', 'marlinwoc']
CHANNEL_LIST = [
    'nislregen',
    'deraltan',
    'gumlong',
    'grandtriskel',
    'Fiesabella',
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
    'yambosoba',
    'theescarboom',
    'dosenpfirsiche',
    'marlinwoc'
]
MSG_FREQ = 1800 # In Seconds

# 1664103600 -> 25. September 2022 13:00:00 GMT+02:00 (Beginn der WoC)
START_TIMESTAMP = datetime.fromtimestamp(1664103600)

# Command texts
HELP_TEXT = "ZACK! Folgende commands sind verfügbar: !website, !faq, !programm, !charity, !donate, !goals, !uptime, !shop, !youtube, !twitter, !musik, !verlosung, !bidwar"
WEBSITE_TEXT = "ZACK! Unsere Website: https://weekofcharity.de/"
FAQ_TEXT = "ZACK! Wichtige Fragen und Antworten in unserem FAQ: https://weekofcharity.de/#faq"
SCHEDULE_TEXT = "ZACK! Hier findet ihr den Zeitplan des Events: https://weekofcharity.de/streams"
CHARITY_TEXT = "ZACK! Hier findet ihr Informationen zur Charity: https://weekofcharity.de/team?id=28"
DONATE_TEXT = "ZACK! Hier könnt ihr donaten: https://www.tipeeestream.com/week-of-charity/donation"
GOALS_TEXT = "ZACK! Hier findet ihr alle Spendenziele: https://weekofcharity.de/#spenden"
SHOP_TEXT = "ZACK! Wenn ihr Interesse an Merch habt, schaut hier rein: https://www.shirtee.com/de/store/weekofcharity/"
YOUTUBE_TEXT = "ZACK! Unser YouTube-Kanal für die Aufzeichnungen: https://www.youtube.com/channel/UCtDccnVlCVBNBo-icr13dfQ"
TWITTER_TEXT = "ZACK! Hier gibt es die neusten Tweets: https://twitter.com/WeekOfCharity"


MUSIK_TEXT = "ZACK! Die Musik für dieses Jahr wurde von amy und mioh gemacht: https://kleeder.bandcamp.com/album/week-of-charity-2022-soundtrack/"
VERLOSUNG_TEXT = "ZACK! Wie ihr an Verlosungen teilnehmen könnt, erfahrt ihr im FAQ auf unserer Website: https://weekofcharity.de/#faq"
BIDWAR_TEXT = "ZACK! Eugen färbt sich die Haare nach eurem Wunsch! Dies könnt ihr in Form von Donations beeinflussen. Mehr Infos in unserem FAQ: https://weekofcharity.de/#faq"

# Other texts
HELLO_TEXT = "ZACK! Hallo, ich bin ChessterBot! Mit '!help' kannst du dir alle verfügbaren Commands anzeigen lassen."
AUSTRIA_HELLO_TEXT = "ZACKL! Griaß di, i bin der ChessterBot! Mit '!help' konnst du dir olle verfügboren Commands anzeigen lossen."
BAYRISCH_HELLO_TEXT = "ZACK! Servus, i bin ChessterBot! Mit '!help' konnst du dir alle verfügbaren Commands ozoagn lassn."
SCHWEIZER_HELLO_TEXT = "ZAGG! Grüezi, ig heisse ChessterBot! Mit '!help' chasch dir alli verfüegbare Commands azeige loh."
LUXEMBURGISCH_HELLO_TEXT = "ZACK! Moien, ech sinn den ChessterBot! Mat '!help' kanns du dir all disponible Commands weisen loossen."

SCHEDULED_MESSAGES = [WEBSITE_TEXT, SCHEDULE_TEXT, DONATE_TEXT, SHOP_TEXT, TWITTER_TEXT]


def woc_format_time(td):
    if td.days == 0 and td.seconds == 0:
        return "ZACK! Die Week of Charity hat gerade begonnen!"
    
    if td.days < 0:
        return "ZACK! Die Week of Charity liegt in der Zukunft!"

    seconds = td.seconds % 60
    minutes = math.floor(td.seconds / 60) % 60
    hours = math.floor(td.seconds / 3600)
    days = td.days

    output = "ZACK! Die Week of Charity läuft bereits seit "

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

class Bot(commands.Bot):

    def __init__(self, hello_msg):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.hello_msg = hello_msg
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=CHANNEL_LIST)

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
                await channel.send(HELLO_TEXT)
                print("Sent hello message @ ({})".format(c))

        while True:
            # Calculate time until next scheduled message.
            s = MSG_FREQ - time.time() % MSG_FREQ
            print("Es sind noch {} Sekunden zur nächsten Nachricht.".format(s))
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
                    print("Sent scheduled message to live channel {}".format(s.user.name))

    async def event_message(self, msg):
        if msg.echo:
            print('[ChessterBot] @ ({}): "{}"'.format(msg.channel.name, msg.content))
            return
        print('[{}] @ ({}): "{}"'.format(msg.author.name, msg.channel.name, msg.content))
        await self.handle_commands(msg)
    
    ####################################

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        await ctx.send(woc_format_time(datetime.now() - START_TIMESTAMP))

    @commands.command(aliases=["commands"])
    async def help(self, ctx: commands.Context):
        await ctx.send(HELP_TEXT)

    ####################################

    # Basic chat commands
    @commands.command()
    async def faq(self, ctx: commands.Context):
        await ctx.send(FAQ_TEXT)

    @commands.command(aliases=["merch"])
    async def shop(self, ctx: commands.Context):
        await ctx.send(SHOP_TEXT)

    @commands.command()
    async def charity(self, ctx: commands.Context):
        await ctx.send(CHARITY_TEXT)

    @commands.command(aliases=["programm", "program", "zeitplan"])
    async def schedule(self, ctx: commands.Context):
        await ctx.send(SCHEDULE_TEXT)

    @commands.command()
    async def twitter(self, ctx: commands.Context):
        await ctx.send(TWITTER_TEXT)

    @commands.command(aliases=["donations", "donation", "spenden", "spende"])
    async def donate(self, ctx: commands.Context):
        await ctx.send(DONATE_TEXT)

    @commands.command(aliases=["yt"])
    async def youtube(self, ctx: commands.Context):
        await ctx.send(YOUTUBE_TEXT)

    @commands.command(aliases=["donationgoals", "goal", "spendenziele", "spendenziel", "ziele"])
    async def goals(self, ctx: commands.Context):
        await ctx.send(GOALS_TEXT)

    @commands.command(aliases=["webseite", "seite", "site", "about", "info", "woc"])
    async def website(self, ctx: commands.Context):
        await ctx.send(WEBSITE_TEXT)
    
    @commands.command(aliases=["musik", "56"])
    async def music(self, ctx: commands.Context):
        await ctx.send(MUSIK_TEXT)

    @commands.command(aliases=["verlosungen", "gewinnspiel"])
    async def verlosung(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_TEXT)
    
    @commands.command(aliases=["haare", "eugen", "eugenshaare"])
    async def bidwar(self, ctx: commands.Context):
        await ctx.send(BIDWAR_TEXT)

    @commands.command()
    async def hallo(self, ctx: commands.Context):
        await ctx.send(HELLO_TEXT)

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
    

if __name__ == '__main__':
    print("Initialize ChessterBot...")
    parser = argparse.ArgumentParser(description='Week of Charity 2022 Twitch Chat Bot "ChessterBot".')
    parser.add_argument('-hello', '--hello_msg', default=False, action='store_true', help='Enable "Hello Message" in all chats the bot loggs into.')
    args = parser.parse_args()
    print("Hello Enabled {}".format(args.hello_msg))

    bot = Bot(args.hello_msg)
    print("Starting ChessterBot...")
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.