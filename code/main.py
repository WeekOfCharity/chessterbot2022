# TODO:
# - Automatisch reconnecten bei Verbindungsverlust
# - Git outfiguren sodass Änderungen schnell möglich sind

# - Richtigen geplanten START_TIMESTAMP ändern
# - Liste aller Kanäle adden
# - Längerer Test auf mehreren Kanälen

from twitchio.ext import commands
from datetime import *
import time
import math
import asyncio

ACCESS_TOKEN = "713jpa4s5jqa5inxf2zlxwlcpynj5r"
TEST_CHANNEL_LIST = [
    'binakleinerals3',
    'marlinwoc'
]
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

# 1664031600 -> 24. September 2022 17:00:00 GMT+02:00
START_TIMESTAMP = datetime.fromtimestamp(1656777593)

# Command texts
HELP_TEXT = "ZACK! Folgende commands sind verfügbar: website, faq, schedule, charity, donate, goals, uptime, shop, youtube, twitter, musik"
FAQ_TEXT = "ZACK! Wichtige Fragen und Antworten in unserem FAQ: https://weekofcharity.de/#faq"
SHOP_TEXT = "ZACK! Wenn ihr Interesse an Merch habt, schaut hier rein: https://www.shirtee.com/de/store/weekofcharity/"
CHARITY_TEXT = "ZACK! Hier findet ihr Informationen zur Charity: https://weekofcharity.de/"
SCHEDULE_TEXT = "ZACK! Hier findet ihr den Zeitplan des Events: https://weekofcharity.de/"
TWITTER_TEXT = "ZACK! Hier gibt es die neusten Tweets: https://twitter.com/WeekOfCharity"
DONATE_TEXT = "ZACK! Hier könnt ihr donaten: https://www.tipeeestream.com/week-of-charity/donation"
YOUTUBE_TEXT = "ZACK! Unser YouTube-Kanal für die Aufzeichnungen: https://www.youtube.com/channel/UCtDccnVlCVBNBo-icr13dfQ"
GOALS_TEXT = "ZACK! Hier findet ihr alle Spendenziele: https://weekofcharity.de/"
WEBSITE_TEXT = "ZACK! Unsere Website: https://weekofcharity.de/"
MUSIK_TEXT = "ZACK! Musik: https://kleeder.bandcamp.com/album/week-of-charity-2022-soundtrack/"
VERLOSUNG_TEXT = "ZACK! Wie ihr an Verlosungen teilnehmen könnt, erfahrt ihr im FAQ auf unserer Website: https://weekofcharity.de/"

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

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=CHANNEL_LIST)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        while True:
            # Calculate time until next scheduled message.
            s = MSG_FREQ - time.time() % MSG_FREQ
            print("Es sind noch {} Sekunden zur nächsten Nachricht.".format(s))
            await asyncio.sleep(s)
            
            # Get a list of all streams that are currently live.
            fetch_streams_task = asyncio.create_task(self.fetch_streams(user_logins=CHANNEL_LIST))
            await fetch_streams_task
            streams = fetch_streams_task.result()

            # Send a message to all live channels
            for s in streams:
                if s.type == "live":
                    channel = self.get_channel(s.user.name)
                    # TODO: Other scheduled messages?
                    await channel.send(WEBSITE_TEXT)
                    print("Sent scheduled message to live channel {}".format(s.user.name))

    async def event_message(self, msg):
        if msg.echo:
            return
        print("{}: {}".format(msg.author.name, msg.content))
        await self.handle_commands(msg)
    
    ####################################

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        await ctx.send(woc_format_time(datetime.now() - START_TIMESTAMP))

    @commands.command()
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

    @commands.command(aliases=["goal", "spendenziele", "spendenziel"])
    async def goals(self, ctx: commands.Context):
        await ctx.send(GOALS_TEXT)

    @commands.command(aliases=["webseite", "seite", "site", "about", "info", "woc"])
    async def website(self, ctx: commands.Context):
        await ctx.send(WEBSITE_TEXT)
    
    @commands.command(aliases=["musik"])
    async def music(self, ctx: commands.Context):
        await ctx.send(MUSIK_TEXT)

    @commands.command()
    async def verlosung(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_TEXT)

if __name__ == '__main__':
    bot = Bot()
    print("Starting ChessterBot...")
    bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.