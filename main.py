import datetime
from twitchio.ext import commands
import sqlite3
import mysql.connector
from termcolor import colored
from classes.viewer import Viewer

# DB connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="toxicity_check"
)
mycursor = mydb.cursor()
message_pack_length = 100
# on rajoute un hours_delta pour correspondre au fuseau horraire, parceque je sais pas utiliser les datetime python

hours_delta = 1
channels_color = {"ponce" : 'magenta',
                  "otplol_" : 'red',
                  "chap_gg" : 'blue',
                  'sardoche' : "green",
                  'amouranth' : 'yellow',
                  'gotaga' : 'cyan'}

messages = []
messages_vals = []
def save_message():
    # REQUETE SQL ###################################################################
    sql = "INSERT INTO message (content, viewer, channel, viewer_color, created_at) VALUES (%s, %s, %s, %s, %s)"

    for message in messages :
        messages_vals.append((message.content, message.author.name, message.channel.name, message.author.color, message.timestamp+ datetime.timedelta(hours = hours_delta)))


    mycursor.executemany(sql, messages_vals)

    mydb.commit()

    # Clear le tableau messages une fois envoyé
    messages.clear()
    messages_vals.clear()

viewers = []
viewers_vals = []
def save_viewers():
    sql = "REPLACE INTO viewer (name, updated_at) VALUES (%s, %s);"
    for viewer in viewers :
        viewers_vals.append( (viewer.name, viewer.updated_at))
    mycursor.executemany(sql, viewers_vals)
    mydb.commit()

     # Clear le tableau viewers une fois envoyé
    viewers.clear()
    viewers_vals.clear()

def save():
    save_message()
    save_viewers()

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='oauth:osmqsanyv3s1k8t0pvw3we6eslqjgi', prefix='?', initial_channels=['Sardoche'])
        #super().__init__(token='oauth:osmqsanyv3s1k8t0pvw3we6eslqjgi', prefix='?', initial_channels=['ponce', 'otplol_', 'chap_gg', 'sardoche', 'amouranth', 'gotaga', 'DeusKiwi'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_mode(self, Channel, User, status: str):
        print("#################### MODERATION #################")
        print("chaine : " + str(Channel))
        print("User : " + str(User))
        print("status : " + str(status))




    async def event_message(self, message) -> None:

        viewer = Viewer(message.author.name, message.timestamp + datetime.timedelta(hours = hours_delta))
        viewers.append(viewer)

        color = 'white'

        if message.channel.name in channels_color:
            color = channels_color[message.channel.name]


        print("[" + str(len(messages)) + "] " + colored(str(message.author.name), color) + " : " + str(message.content))

        messages.append(message)

        if(len(messages) >= message_pack_length ):
            print("#################### Ca fait 100 messages #################")
            save()


    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

bot = Bot()
bot.run()
