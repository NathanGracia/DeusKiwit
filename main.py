from twitchio.ext import commands
import sqlite3
import mysql.connector
from termcolor import colored


# DB connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="deuskiwit"
)
mycursor = mydb.cursor()
message_pack_length = 100

channels_color = {"ponce" : 'magenta',
                  "otplol_" : 'red',
                  "chap_gg" : 'blue',
                  'sardoche' : "green",
                  'amouranth' : 'yellow',
                  'gotaga' : 'cyan'}

messages = []
vals = []
def save(messages):
    # REQUETE SQL ###################################################################
    sql = "INSERT INTO messages (content, user, channel, user_color, created_at) VALUES (%s, %s, %s, %s, %s)"

    for message in messages :
        vals.append((message.content, message.author.name, message.channel.name, message.author.color, message.timestamp))


    mycursor.executemany(sql, vals)

    mydb.commit()

    # Clear le tableau messages une fois envoyé
    messages.clear()
    vals.clear()

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='oauth:osmqsanyv3s1k8t0pvw3we6eslqjgi', prefix='?', initial_channels=['ponce', 'otplol_', 'chap_gg', 'sardoche', 'amouranth', 'gotaga'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message) -> None:
        color = 'white'
        if message.channel.name in channels_color:
            color = channels_color[message.channel.name]
        print("[" + str(len(messages)) + "] " + colored(str(message.author.name), color) + " : " + str(message.content))
        messages.append(message)

        if(len(messages) >= message_pack_length ):
            print("#################### Ca fait 100 messages #################")
            save(messages)


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
