# ChessterBot created by Bina and Marlin for the Week of Charity 2022

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

# 1664103600 -> 25. September 2022 13:00:00 GMT+02:00 (Beginn der WoC2022)
START_TIMESTAMP = datetime.fromtimestamp(1664103600)

# Command texts
HELP_TEXT = "ZACK! Folgende commands sind verfügbar: !website, !faq, !programm, !charity, !donate, !goals, !uptime, !shop, !socials, !youtube, !twitter, !tiktok, !musik, !verlosung, !bidwar"
WEBSITE_TEXT = "ZACK! Unsere Website: https://weekofcharity.de/"
FAQ_TEXT = "ZACK! Wichtige Fragen und Antworten in unserem FAQ: https://weekofcharity.de/#faq"
SCHEDULE_TEXT = "ZACK! Hier findet ihr den Zeitplan des Events: https://weekofcharity.de/streams"
CHARITY_TEXT = "ZACK! Hier findet ihr Informationen zur Charity: https://weekofcharity.de/team?id=28"
DONATE_TEXT = "ZACK! Hier könnt ihr donaten: https://www.tipeeestream.com/week-of-charity/donation"
GOALS_TEXT = "ZACK! Hier findet ihr alle Spendenziele: https://weekofcharity.de/#spenden"
SHOP_TEXT = "ZACK! Wenn ihr Interesse an Merch habt, schaut hier rein: https://www.shirtee.com/de/store/weekofcharity/"
SOCIALS_TEXT = "ZACK! Folgt uns auf YouTube: https://www.youtube.com/channel/UCtDccnVlCVBNBo-icr13dfQ - Twitter: https://twitter.com/WeekOfCharity - TikTok: https://www.tiktok.com/@weekofcharity"
YOUTUBE_TEXT = "ZACK! Unser YouTube-Kanal für die Aufzeichnungen: https://www.youtube.com/channel/UCtDccnVlCVBNBo-icr13dfQ"
TWITTER_TEXT = "ZACK! Hier gibt es die neusten Tweets: https://twitter.com/WeekOfCharity"
TIKTOK_TEXT = "ZACK! Folgt uns auf TikTok für lustige Clips: https://www.tiktok.com/@weekofcharity"
MUSIK_TEXT = "ZACK! Die Musik für dieses Jahr wurde von amy und mioh gemacht: https://kleeder.bandcamp.com/album/week-of-charity-2022-soundtrack/"
VERLOSUNG_TEXT = "ZACK! Wie ihr an Verlosungen teilnehmen könnt, erfahrt ihr im FAQ auf unserer Website: https://weekofcharity.de/#faq"
BIDWAR_TEXT = 'ZACK! Eugen färbt sich die Haare nach eurem Wunsch! Dies könnt ihr in Form von Donations beeinflussen. Die Optionen sind Hellblau/Rosa "Trans", Lila/Gelb "Nonbinary" oder Grün/Pink "Splatoon 2". Mehr Infos in unserem FAQ: https://weekofcharity.de/#faq'
SCHACHSTREAM_TEXT = 'ZACK! Den Plan für den Schachstream findet ihr hier: https://twitter.com/wizomibaby/status/1575933168808386560?t=kEX6klwSywFFnRJnqGIrEw&s=19'

VERLOSUNG_SVEN_TEXT = "Am Ende des Pen and Paper-Abenteuers am Mittwoch könnt ihr einen Key für Wonderdraft gewinnen! Mithilfe dieser Software könnt ihr atemberaubende Karten für eure fiktiven Welten oder auch einfach zum Spaß erstellen!"
VERLOSUNG_EUGEN_TEXT = "Bei Eugen wird eure Switch bereichert! Gewinnen könnt ihr am Dienstag zwischen 04:00-07:00 Uhr Pokémon Schillernde Perle, am Donnerstag zwischen 05:00-08:00 Uhr Paper Mario: The Origami King und am Freitag zwischen 08:00-11:00 Uhr The Legend of Zelda: Skyward Sword HD!"
VERLOSUNG_LISA_TEXT = "Am Ende des Glass Painting Streams könnt ihr das fertige Kunstwerk gewinnen! Ein Stück Week of Charity-Geschichte für euer Wohnzimmer!"
VERLOSUNG_LUCA_TEXT = "Am Donnerstag zwischen 12-15 Uhr könnt ihr hier zwei Steam-Keys für Guts and Goals, den Mix aus Fußball und Beat-em-up, gewinnen! Diese Keys wurden uns extra vom Entwickler zur Verfügung gestellt und werden spontan verlost, also haltet die Ohren offen!"
VERLOSUNG_CHRIS_TEXT = "Auf dem Glücksrad findet man neben einer Ansammlung großartiger Spiele, die von Chris gespielt werden, auch großartige Spiele, die verlost werden! Wenn das Rad darauf landet, wird sofort eine Verlosung abgehalten. Also spendet auf keinen Fall, sonst muss Chris immer wieder drehen!"
VERLOSUNG_FELI_TEXT = "Falls ihr Freude am Kreativen habt, könnt ihr hier 3 Keys für Guts and Goals auf Steam gewinnen. Die Gewinner werden hier nicht per Zufall ermittelt, sondern über die besten Bauten des Minecraft Servers! Schaut für nähere Infos einfach auf dem Server WeekOfCharity.mine-hoster.net vorbei und schaltet ein, wenn Feli am Freitag die Projekte bewertet! Ihr müsst beim Stream nicht anwesend sein, um zu gewinnen."
VERLOSUNG_NOAH_TEXT = "Der Schachstream ist immer voller Highlights, und diesmal gibt es sogar ein Neues obendrauf: Die ersten drei Personen, die Noah in den Zuschauerpartien Matt setzen können, erhalten ihre Wahl aus den Spielen Chess Ultra, UNDERTALE und Slay the Spire! Wer zuerst gewinnt, mahlt zuerst!"
VERLOSUNG_FINALE_TEXT = "Wie ihr an der finalen Verlosung teilnehmt, ist noch geheim!"

# Other texts
HELLO_TEXT = "ZACK! Hallo, ich bin ChessterBot! Mit '!help' kannst du dir alle verfügbaren Commands anzeigen lassen."
AUSTRIA_HELLO_TEXT = "ZACKL! Griaß di, i bin der ChessterBot! Mit '!help' konnst du dir olle verfügboren Commands anzeigen lossen."
BAYRISCH_HELLO_TEXT = "ZACK! Servus, i bin ChessterBot! Mit '!help' konnst du dir alle verfügbaren Commands ozoagn lassn."
SCHWEIZER_HELLO_TEXT = "ZAGG! Grüezi, ig heisse ChessterBot! Mit '!help' chasch dir alli verfüegbare Commands azeige loh."
LUXEMBURGISCH_HELLO_TEXT = "ZACK! Moien, ech sinn den ChessterBot! Mat '!help' kanns du dir all disponible Commands weisen loossen."

SCHALTSEKUNDEN_TEXT = "ZACK! Wenn ihr Interesse an Schaltsekunden habt, schaut hier rein: https://de.wikipedia.org/wiki/Schaltsekunde"

SCHEDULED_MESSAGES = [WEBSITE_TEXT, SCHEDULE_TEXT, DONATE_TEXT, SHOP_TEXT, TWITTER_TEXT]


def woc_format_time(td):
    if td.days == 0 and td.seconds == 0:
        return "ZACK! Die Week of Charity hat gerade begonnen!"
    
    if td.days < 0:
        return "ZACK! Die Week of Charity liegt in der Zukunft!"

    if td.days > 8:
        return "ZACK! Die Week of Charity ist vorbei!"

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
                await channel.send(HELLO_TEXT)
                print("Sent hello message @ ({})".format(c))

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

    @commands.command()
    async def tiktok(self, ctx: commands.Context):
        await ctx.send(TIKTOK_TEXT)

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

    @commands.command(aliases=["VerlosungSven", "verlosungSven"])
    async def verlosungsven(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_SVEN_TEXT)

    @commands.command(aliases=["VerlosungEugen", "verlosungEugen"])
    async def verlosungeugen(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_EUGEN_TEXT)

    @commands.command(aliases=["VerlosungLisa", "verlosungLisa"])
    async def verlosunglisa(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_LISA_TEXT)

    @commands.command(aliases=["VerlosungLuca", "verlosungLuca"])
    async def verlosungluca(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_LUCA_TEXT)

    @commands.command(aliases=["VerlosungChris", "verlosungChris"])
    async def verlosungchris(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_CHRIS_TEXT)

    @commands.command(aliases=["VerlosungFeli", "verlosungFeli"])
    async def verlosungfeli(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_FELI_TEXT)

    @commands.command(aliases=["VerlosungNoah", "verlosungNoah"])
    async def verlosungnoah(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_NOAH_TEXT)

    @commands.command(aliases=["VerlosungFinale", "verlosungFinale"])
    async def verlosungfinale(self, ctx: commands.Context):
        await ctx.send(VERLOSUNG_FINALE_TEXT)

    @commands.command()
    async def socials(self, ctx: commands.Context):
        await ctx.send(SOCIALS_TEXT)

    @commands.command(aliases=["schaltminute", "schaltminuten", "schaltsekunde"])
    async def schaltsekunden(self, ctx: commands.Context):
        await ctx.send(SCHALTSEKUNDEN_TEXT)
    
    @commands.command(aliases=["schach", "schachstreamplan", "schachstreamschedule"])
    async def schachstream(self, ctx: commands.Context):
        await ctx.send(SCHACHSTREAM_TEXT)

if __name__ == '__main__':
    print("Initialize ChessterBot...")
    parser = argparse.ArgumentParser(description='Week of Charity 2022 Twitch Chat Bot "ChessterBot".')
    parser.add_argument('-hello', '--hello_msg', default=False, action='store_true', help='Enable "Hello Message" in all chats the bot loggs into.')
    parser.add_argument('--token', type=str, default='', help='Token for Twitch API.')
    args = parser.parse_args()
    token = args.token

    load_dotenv()

    if len(token) < 1:
        print("Reading Access Token from .env file.")
        token = os.getenv('ACCESS_TOKEN')

    bot = Bot(token, args.hello_msg)
    print("Hello Test-Message in all channels enabled: {}".format(args.hello_msg))
    print("Starting ChessterBot...")
    try:
        bot.run()
    except AuthenticationError:
        # This error handling doesnt work. Idk why, asyncio is weird.
        print("Invalid or no Access Token provided. Use --token to provide the Access Token or set up an .env in the root directory containing the ACCESS_TOKEN field to provide a valid token.")
        exit(1)

# bot.run() is blocking and will stop execution of any below code here until stopped or closed.