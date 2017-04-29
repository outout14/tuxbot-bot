#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Maël — outout"
__licence__ = "WTFPL Licence 2.0"


#################
#   IMPORTS     #
#################
from botassets import *
from botassets.imports import *
client = discord.Client()
status = "dnd"
wikipedia.set_lang("fr")

###########################################
#                                         #
#               LOGGER                    #
#                                         #
###########################################
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s // [%(levelname)s] : %(message)s')
file_handler = RotatingFileHandler('logs/activity.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info(' \n \n New TuxBot instance \n \n')

###########################################
#           OPEN GAME FILE NAME           #
###########################################
game = open('msg/game.txt').read()

#### SQL #####
conn = sqlite3.connect('tuxbot.db') #Connexion SQL

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     userid TEXT,
     username TEXT,
     usermention TEXT,
     os TEXT,
     config TEXT,
     useravatar TEXT,
     userbirth TEXT,
     cidate TEXT,
     pays TEXT
)
""")# Creation table Utilisateur si premiere fois
conn.commit()


###########################################
#                                         #
#             ON_READY                    #
#                                         #
###########################################
@client.event
async def on_ready():
    logger.info('BOT READY !')
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("TuxBot " + version)
    logger.log(logging.DEBUG, 'TuxBot ' + version)
    print(" ")
    print("Pret ! ")
    print("Vous pouvez l'utiliser.")
    await client.change_presence(game=discord.Game(name=game), status=discord.Status(status), afk=False) ## Game set in config.py
    print("Jeu joué : " + game)
    print("Pseudo : " + client.user.name)
    print("ID : " + client.user.id)
    logger.debug('Bot ID : ' + client.user.id)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

###########################################
#                                         #
#             JOIN AND LEAVE              #
#                                         #
###########################################
@client.event
async def on_member_join(member):
    logger.log(logging.INFO, member.name + ' joined the server !')
    server = member.server
    prv = await client.start_private_message(member)
    welcome_msg = random.choice(arrays.wlcm_msgs)
    if member.server.name == "Aide GNU/Linux-fr":
        fmt = 'Bienvenue {0.mention} sur le suberbe serveur discord **' + member.server.name + '** ! Je te conseil de lire #regles pour commencer et te créer une carte d\'identité dans ``#bot`` grâce à la commande ``.ci-register`` et la personnaliser :smile: !'
    else:
        fmt = 'Bienvenue {0.mention} sur le discord **'+ member.server.name +'**, j\'espère que tu passeras un bon moment avec nous !' ##Multi-Server
    await client.send_message(prv, fmt.format(member))
    await client.send_message(member.server.default_channel, "**{0}**".format(welcome_msg.format(member)))
@client.event
async def on_member_remove(member):
    adios_msg = random.choice(arrays.adios_msgs)
    logger.log(logging.INFO, member.name + ' left the server !')
    await client.send_message(member.server.default_channel, "**{0}**".format(adios_msg.format(member)))
###########################################
#                                         #
#             DELETE MESSAGE              #
#                                         #
###########################################
@client.event
async def on_message_delete(message):
    if not message.channel.is_private and not message.author.bot:
        msg_log = open('logs/deleted_msg.log', 'a')
        date = time.localtime(time.time())
        msg_log.write(str(message.author.name) + " (" + message.author.id + ")\n")
        msg_log.write("  -> serveur : " + message.server.name + " \n")
        msg_log.write("  -> date    : " + str(time.strftime("%d %b %Y %H:%M:%S", date)) + "\n")
        msg_log.write("  -> message : " + str(message.content) + "\n")
        msg_log.write("--------------------------------------------------------------------------------------------------\n")
        msg_log.close()

@client.event
async def on_message(message):
###########################################
#                                         #
#             CUSTOMS FUNCTIONS           #
#              BLOCKING AND ...           #
#                                         #
###########################################
    roles = ["bot-commander", "poney"]

    def cmd(cmd_name):
        if not message.channel.is_private and not message.author.bot:
            return message.content.startswith(prefix + cmd_name)

    def authadmin():
        role = message.author.roles
        print("A")
        try:
            if str(role[0]) in roles or str(role[1]) in roles or str(role[2]) in roles or str(role[3]) in roles or str(role[4]) in roles:
                return True
            else:
                return False
        except IndexError:
            return False

    if message.channel.is_private and not message.author.bot:
        await client.send_message(message.channel, "Désolé mais mon papa m'a dit de ne pas parler par Message Privé, viens plutot sur un serveur discord !")


###########################################
#                                         #
#                ADMIN COMMANDS           #
#                                         #
###########################################

    if cmd("sendlogs"):
        if authadmin:
            wait = await client.send_message(message.channel, message.author.mention + " Le contenue du fichier log est entrain d'être envoyé... Veuillez patienter, cela peut prendre du temps !")
            await client.send_file(message.author, fp="logs/activity.log", filename="activity.log", content="Voci mon fichier ``activity.log`` comme demandé !", tts=False)
            await client.edit_message(wait, message.author.mention + " C'est bon vous venez de recevoir par message privé mon fichier de logs")
        else:
            await client.send_message(message.channel, "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

    elif cmd("say"): #Control
        if authadmin():
            args = message.content.split("say ")
            try:
                await client.send_message(message.channel, args[1])
                logger.info(message.author.name + ' ordered TuxBot to say : ' + args[1])
                await client.delete_message(message)
            except IndexError:
                await client.send_message(message.author, "**[ERREUR]** Merci de fournir le paramètre du message à dire, je ne suis pas dans ta tête !")
                await client.delete_message(message)
        else:
            await client.send_message(message.channel, message.author.mention + "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

    elif cmd("clear"):
        if authadmin:
            try:
                args = message.content.split("clear ")
                argument = int(args[1])
                argument = argument+1
                logger.info(message.author.name + ' ordered TuxBot to remove ' + args[1] + ' messages')
                deleted = await client.purge_from(message.channel, limit=argument)
                await client.send_message(message.author, args[1] + " messages ont bien été supprimés")
            except IndexError:
                await client.send_message(message.author, "**[ERREUR]** Merci de fournir le paramètre du nombre de message à supprimer, je ne suis pas dans ta tête !")
                await client.delete_message(message)
        else:
            await client.send_message(message.channel, message.author.mention + "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

    elif cmd("changegame"):
        if authadmin:
            args = message.content.split("changegame ")
            try:
                ngame = open('msg/game.txt','w')
                ngame.write(args[1])
                ngame.close()
                rgame = open('msg/game.txt').read()
                await client.change_presence(game=discord.Game(name=rgame), status=discord.Status(status), afk=False)
                await client.send_message(message.author, "Mon jeu joué à bien été changé en : " + rgame)
                await client.delete_message(message)
                logger.info(message.author.name + ' changed the game played from tuxbot to : ' + args[1])
            except IndexError:
                await client.send_message(message.author, "**[ERREUR]** Merci de fournir le paramètre du jeu que je dois jouer, je ne suis pas dans ta tête !")
                await client.delete_message(message)
        else:
            await client.send_message(message.channel, message.author.mention + "[**ERREUR**] Vous n'avez pas la permission d'executer cette commande")

###########################################
#                                         #
#            WWW COMMANDS                 #
#                                         #
###########################################
    elif cmd("search docubuntu"):
        args_ = message.content.split(" ")
        await client.send_typing(message.channel)
        try:
           msg = await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de parcourir le WorldWideWeb avec comme terme de recherche " + args_[2] + ", et ça peut prendre du temps ! ")
           html = urllib.request.urlopen("https://doc.ubuntu-fr.org/" + args_[2]).read()
           if "avez suivi un lien" in str(html):
              await client.edit_message(msg, message.author.mention + " :sob: Oh non ! Cette page n'existe pas sur la doc ubuntu-fr. Mais vous pouvez commencer à la rédiger ! https://doc.ubuntu-fr.org/"+ args_[2])
           else:
              await client.edit_message(msg, message.author.mention + " :ok_hand: Trouvé ! Voici la page ramenant à votre recherche https://doc.ubuntu-fr.org/"+ args_[2])
        except IndexError:
               await client.edit_message(msg, message.author.mention + " **Erreur** : veuillez entrer un terme de recherche !")

    elif cmd("search wikileaks"):
        args_ = message.content.split(" ")
        await client.send_typing(message.channel)
        try:
           msg = await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de parcourir le WorldWideWeb avec comme terme de recherche " + args_[2] + ", et ça peut prendre du temps ! ")
           await client.send_typing(message.channel)
           html = urllib.request.urlopen("https://search.wikileaks.org/?query=" + args_[2] + "#results").read()
           await client.delete_message(msg)
           if "0 results" in str(html):
               await client.edit_message(msg, message.author.mention + " :sob: Oh non ! Aucun élément ne correspond de pres ou de loin a votre recherche.")
           else:
               await client.edit_message(msg, message.author.mention + " :ok_hand: Trouvé ! Le résultat de votre recherche est ici => https://search.wikileaks.org/?query=" + args_[2] + "#results")
        except IndexError:
               await client.edit_message(msg, message.author.mention + " **Erreur** : veuillez entrer un terme de recherche !")

    elif cmd("search wikipedia"):

        try:
            args = message.content.split("search wikipedia")
            wait = await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de parcourir Wikipedia avec comme terme de recherche " + args[1] + ", et ça peut prendre du temps ! ")
            results = wikipedia.search(args[1])
            nbmr = 0
            msg = ""

            for value in results:
                nbmr = nbmr + 1
                msg = msg + "**{}**: {} \n".format(str(nbmr), value)

            em = discord.Embed(title='Résultats de : ' + args[1], description = msg, colour=0x4ECDC4)
            em.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/2/26/Paullusmagnus-logo_%28large%29.png")
            await client.delete_message(wait)
            final = await client.send_message(message.channel, embed=em)

            for emoji in arrays.array_emoji:
               await client.add_reaction(final, emoji)

            res = await client.wait_for_reaction(message=final, user=message.author)

            for emoji in arrays.array_emoji:
                num_emoji = arrays.array_emoji.index(emoji)
                if res.reaction.emoji == emoji:
                    args_ = results[num_emoji]

            try:
                await client.delete_message(final)
                await client.send_typing(message.channel)
                wait = await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de chercher sur Wikipedia " + args_ + ", et ça peut prendre du temps ! ")
                wp = wikipedia.page(args_)
                wp_contenu = wp.summary[:200] + "..."
                em = discord.Embed(title='Wikipedia : ' + wp.title, description = "{} \n _Lien_ : {} ".format(wp_contenu, wp.url), colour=0x9B59B6)
                em.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/2/26/Paullusmagnus-logo_%28large%29.png")
                em.set_footer(text = "Source : Wikipedia")
                await client.delete_message(wait)
                await client.send_message(message.channel, embed=em)
            except wikipedia.exceptions.PageError:
                await client.delete_message(msg)
                await client.send_message(message.channel, message.author.mention + " **Erreur interne** : une erreur interne est survenue, si cela ce reproduit contactez votre administrateur ou faites une Issue sur github !")
            except wikipedia.exceptions.DisambiguationError:
                await client
            except UnboundLocalError:
                await client.send_message(message.channel, message.author.mention + " **Erreur** : veuillez choisir une réaction valide !")

        except IndexError:
            await client.send_message(message.channel, message.author.mention + " **Erreur** : veuillez entrer un terme de recherche !")

    elif cmd("yt"):
        await client.send_typing(message.channel)
        chaineyt = random.choice(arrays.youtube)
        ytname = chaineyt.split(",")
        yturl = chaineyt.split(": ")
        ytname = ytname[0]

        text = "Je peux te conseiller cette chaîne youtube : " + chaineyt
        em = discord.Embed(title='Youtube Discover', description=text, colour=0xCD201F)
        em.set_author(name=ytname, icon_url="http://outout.tech/tuxbot_files/loading.gif")
        msg = await client.send_message(message.channel, embed=em)

        ##GET ICON##
        html_doc = urllib.request.urlopen(yturl[1]).read()
        soup = BeautifulSoup(html_doc, "lxml")
        getatr = soup.find_all("img", { "class" : "appbar-nav-avatar" }, ["src"])
        getatr = str(getatr)
        getatr = getatr.split('"')
        em.set_author(name=ytname, icon_url=getatr[7])
        await client.edit_message(msg, embed=em)

###########################################
#                                         #
#            BASICS COMMANDS              #
#                                         #
###########################################
    if cmd("afk"):##AFK
        msg = await client.send_message(message.channel, message.author.mention + " s'absente de discord quelques instants...")
        await client.delete_message(message)

    elif cmd("back"): ##BACK
        await client.send_message(message.channel, message.author.mention + " est de retour parmi nous (il a recussité !)")
        await client.delete_message(message)

    elif cmd("ping"): #PING
       t1 = time.perf_counter()
       await client.send_typing(message.channel)
       t2 = time.perf_counter()
       result = round((t2-t1)*1000)
       if int(result) >=200:
          em = discord.Embed(title="Ping : " + str(result) + "ms", description="... c'est quoi ce ping !", colour=0xFF1111)
          await client.send_message(message.channel, embed=em)
       elif int(result) > 100 and int(result) < 200:
          em = discord.Embed(title="Ping : " + str(result) + "ms", description="Ca va, ça peut aller, mais j'ai l'impression d'avoir 40 ans !", colour=0xFFA500)
          await client.send_message(message.channel, embed=em)
       elif int(result) <= 100:
          em = discord.Embed(title="Ping : " + str(result) + "ms", description="Wow c'te vitesse de réaction, je m'épate moi-même !",colour=0x11FF11)
          await client.send_message(message.channel, embed=em)

    elif cmd("coin"): ##PIECE
        piece = random.choice(["Pile", "Face", "... Heu, je l'ai perdu !", "Pile, j'ai gagné !", "Enfaite c'est quoi pile, c'est quoi face ?"])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, "La piece est retombé sur " + piece)

    elif cmd("joke"): ##Joke
        joke = random.choice(arrays.jokes)
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + " " + joke)

    elif cmd("ethylotest"):
        resultat = random.choice(arrays.policier)
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + resultat)

    elif cmd('randomcat'): ##Cat
        r = requests.get('http://random.cat/meow.php')
        await client.send_message(message.channel, message.author.mention + " " + r.json()['file'])

    elif cmd('pokemon'): ##Pokemon
        await client.send_typing(message.channel)
        poke1 = random.choice(arrays.pokemon)
        poke2 = random.choice(arrays.pokemon)
        win = random.choice([str(poke1),str(poke2)])
        msg1 = await client.send_message(message.channel, '**Le combat Commence !**')
        msg2 = await client.send_message(message.channel, '📢 **Présentateur** : Les combatants sont : ' + str(poke1) + ' Contre ' + str(poke2))
        msg3 = await client.send_message(message.channel, '*Narateur : Le combat se déroule...*')
        await client.send_typing(message.channel)
        await asyncio.sleep(5)
        msg4 = await client.send_message(message.channel, '**📢 Présentateur** : Le gagnant est..... ')
        await client.send_typing(message.channel)
        await asyncio.sleep(1)
        msg5 = await client.send_message(message.channel, '**📢 Présentateur** : **' + str(win) + '**')

    if cmd("servers-list"):
        nbmr = 0
        msg = ""
        for serveur in list(client.servers):
            nbmr = nbmr + 1
            msg = msg + "=> **{}** \n".format(serveur.name)
        msg = msg + "{} se trouve sur **{} serveur(s)** au total !".format(client.user.name, nbmr)
        em = discord.Embed(title='Liste des serveurs où se trouve ' + client.user.name, description=msg, colour=0x36D7B7)
        em.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await client.send_message(message.channel, embed=em)

    elif cmd("count-members"):
        nbmr = 0
        for name in list(client.get_all_members()):
            nbmr = nbmr + 1
        msg = "Il y'a **{} membres** sur le serveur Discord **{}**".format(nbmr, message.server.name)
        em = discord.Embed(title='Compteur de membres', description=msg, colour=0x9A12B3)
        await client.send_message(message.channel, embed=em)

###########################################
#                                         #
#                CLOCK                    #
#                                         #
###########################################
    elif cmd('clock'):
        args = message.content.split("clock ")
        args = [element.upper() for element in args]
        args_ = [element.lower() for element in args]
        then = datetime.datetime.now(pytz.utc)
        form = '%H heures %M'
        try:
            argument = args[1]
            if args[1] == "MONTREAL":
                utc = then.astimezone(pytz.timezone('America/Montreal'))
                site = "http://ville.montreal.qc.ca/"
                img = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Rentier_fws_1.jpg"
                country = "au Canada, Québec"
                description = "Montréal est la deuxième ville la plus peuplée du Canada. Elle se situe dans la région du Québec"
            elif args[1] == "VANCOUVER":
                utc = then.astimezone(pytz.timezone('America/Vancouver'))
                site = "http://vancouver.ca/"
                img = "https://upload.wikimedia.org/wikipedia/commons/f/fe/Dock_Vancouver.JPG"
                country = "au Canada"
                description = "Vancouver, officiellement City of Vancouver, est une cité portuaire au Canada"
            elif args[1] == "NEW-YORK" or args[1] == "N-Y":
                utc = then.astimezone(pytz.timezone('America/New_York'))
                site = "http://www1.nyc.gov/"
                img = "https://upload.wikimedia.org/wikipedia/commons/e/e3/NewYork_LibertyStatue.jpg"
                country = "aux U.S.A."
                description = "New York, est la plus grande ville des États-Unis en termes d'habitants et l'une des plus importantes du continent américain. "
            elif args[1] == "LOSANGELES" or args[1] == "L-A" or args[1] == "LA" or args[1] == "LACITY":
                utc = then.astimezone(pytz.timezone('America/Los_Angeles'))
                site = "https://www.lacity.org/"
                img = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/LA_Skyline_Mountains2.jpg/800px-LA_Skyline_Mountains2.jpg"
                country = "aux U.S.A."
                description = "Los Angeles est la deuxième ville la plus peuplée des États-Unis après New York. Elle est située dans le sud de l'État de Californie, sur la côte pacifique."
            elif args[1] == "PARIS":
                utc = then.astimezone(pytz.timezone('Europe/Paris'))
                site = "http://www.paris.fr/"
                img = "https://upload.wikimedia.org/wikipedia/commons/a/af/Tour_eiffel_at_sunrise_from_the_trocadero.jpg"
                country = "en France"
                description = "Paris est la capitale de la France. Elle se situe au cœur d'un vaste bassin sédimentaire aux sols fertiles et au climat tempéré, le bassin parisien."
            elif args[1] == "BERLIN":
                utc = then.astimezone(pytz.timezone('Europe/Berlin'))
                site = "http://www.berlin.de/"
                img = "https://upload.wikimedia.org/wikipedia/commons/9/91/Eduard_Gaertner_Schlossfreiheit.jpg"
                country = "en Allemagne"
                description = "Berlin est la capitale et la plus grande ville d'Allemagne. Située dans le nord-est du pays, elle compte environ 3,5 millions d'habitants. "
            elif args[1] == "BERN" or args[1] == "ZURICH" or args[1] == "BERNE":
                utc = then.astimezone(pytz.timezone('Europe/Zurich'))
                site = "http://www.berne.ch/"
                img = "https://upload.wikimedia.org/wikipedia/commons/d/db/Justitia_Statue_02.jpg"
                country = "en Suisse"
                description = "Berne est la cinquième plus grande ville de Suisse et la capitale du canton homonyme. Depuis 1848, Berne est la « ville fédérale »."
            elif args[1] == "TOKYO":
                utc = then.astimezone(pytz.timezone('Asia/Tokyo'))
                site = "http://www.gotokyo.org/"
                img = "https://upload.wikimedia.org/wikipedia/commons/3/37/TaroTokyo20110213-TokyoTower-01.jpg"
                country = "au Japon"
                description = "Tokyo, anciennement Edo, officiellement la préfecture métropolitaine de Tokyo, est la capitale du Japon."
            elif args[1] == "MOSCOU":
                utc = then.astimezone(pytz.timezone('Europe/Moscow'))
                site = "https://www.mos.ru/"
                img = "https://upload.wikimedia.org/wikipedia/commons/f/f7/Andreyevsky_Zal.jpg"
                country = "en Russie"
                description = "Moscou est la capitale de la Fédération de Russie et la plus grande ville d'Europe. Moscou est situé sur la rivière Moskova. "
            try:
                if args[1] == "LIST":
                    await client.send_typing(message.channel)
                    text = open('msg/clocks.md').read()
                    em = discord.Embed(title='Liste des Horloges', description=text.format(prefix), colour=0xEEEEEE)
                    await client.send_message(message.channel, embed=em)
                else:
                    tt = utc.strftime(form)
                    em = discord.Embed(title='Heure à ' + args_[1].title(), description="A [{}]({}) {}, Il est **{}** ! \n {} \n _source des images et du texte : [Wikimedia foundation](http://commons.wikimedia.org/)_".format(str(args[1]), site, str(country), str(tt), str(description)), colour=0xEEEEEE)
                    em.set_thumbnail(url = img)
                    await client.send_message(message.channel, embed=em)
            except UnboundLocalError:
                 await client.send_message(message.channel, message.author.mention + " **[ERREUR]** Ville inconnue, ``.clock list`` pour afficher les villes disponibles !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " **[ERREUR]** Veuillez sélectionner une ville dans ``.clock list`` !")

###################
# IDENTIY SYSTEM  #
###################

    elif cmd("ci-register"):
        cursor.execute("""INSERT INTO users(userid, username, usermention, useravatar, userbirth, cidate) VALUES(?, ?, ?, ?, ?, ?)""", (message.author.id, message.author.name, message.author.mention, message.author.avatar_url, message.author.created_at, message.timestamp))
        conn.commit()
        await client.send_message(message.channel, message.author.mention + "> **Votre carte d'intentité à été enregistrée !** Pour plus d'informations sur le système de carte d'indentité, tapez la commande ``{}ci-info`` !".format(prefix))

    elif cmd("ci-setos"):
        try:
            args = message.content.split("ci-setos ")
            cursor.execute("""UPDATE users SET os = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("ci-setconf"):
        try:
            args = message.content.split("ci-setconf ")
            cursor.execute("""UPDATE users SET config = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("ci-setnation"):
        try:
            args = message.content.split("ci-setnation ")
            cursor.execute("""UPDATE users SET pays = ? WHERE usermention = ?""", (args[1], message.author.mention))
            conn.commit()
            await client.send_message(message.channel, message.author.mention + " l'information à bien été modifié sur votre carte d'identité !")
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")

    elif cmd("ci-info"):
        cinfomd = open('msg/ci-info.md').read()
        em = discord.Embed(title='Aide sur la carte d\'identité', description=cinfomd.format(prefix), colour=0xDEADBF)
        await client.send_message(message.channel, embed=em)

    elif cmd("ci"):
        try:
            args = message.content.split("ci ")
            cursor.execute("""SELECT userid, username, os, usermention, useravatar, userbirth, cidate, config, pays FROM users WHERE usermention=?""", (args[1],))
            result = cursor.fetchone()
            if not result:
                await client.send_message(message.channel, message.author.mention + "> Désolé mais {} n'a pas fait enregistrer sa Carte d'indentité".format(args[1]))
            else:
                userid = result[0]
                username = result[1]
                if not result[2]:
                    os = "Non renseigné"
                else:
                    os = result[2]

                if not result[7]:
                    config = "Non renseigné"
                else:
                    config = result[7]

                if not result[8]:
                    pays = "Non renseigné"
                else:
                    pays = result[8]

                useravatar = result[4]
                userbirth = result[5]
                cidate = result[6]
                userbirth = userbirth.split(" ")
                cidate = cidate.split(" ")

                em_content = open('msg/identity.md').read()
                em = discord.Embed(title='Carte d\'Identité de '+ username, description=em_content.format(userid, username, os, useravatar, userbirth[0], cidate[0], config, pays), colour=0xDEADBF)
                em.set_author(name=username, icon_url=useravatar)
                await client.send_message(message.channel, embed=em)
        except IndexError:
            await client.send_message(message.channel, message.author.mention + " [**ERREUR**] : Veuillez argumenter la commande !")


###########################################
#                                         #
#          HELP AND FIX COMMANDS          #
#                                         #
###########################################
    elif cmd('help'): ##HELP
        await client.send_typing(message.channel)
        text = open('msg/help.md').read()
        em = discord.Embed(title='Liste des Commandes', description=text.format(prefix), colour=0x89C4F4)
        await client.send_message(message.channel, embed=em)

    elif cmd("info"): ##info
        text = open('msg/info.md').read()
        em = discord.Embed(title='Informations sur ' + client.user.name, description=text, colour=0x89C4F9)
        await client.send_message(message.channel, embed=em)

    elif cmd('search help'): ##Search
        text = open('msg/search.md').read()
        em = discord.Embed(title='Sites de recherche', description=text.format(prefix), colour=0x4ECDC4)
        await client.send_message(message.channel, embed=em)

    elif cmd('github'): ##Link to github
        await client.send_typing(message.channel)
        text = "How tu veux voir mon repos Github pour me disséquer ? Pas de soucis ! Je suis un Bot, je ne ressens pas la douleur !\n https://github.com/outout14/tuxbot-bot"
        em = discord.Embed(title='Repos TuxBot-Bot', description=text, colour=0xE9D460)
        em.set_author(name='Outout', icon_url="https://avatars0.githubusercontent.com/u/14958554?v=3&s=400")
        await client.send_message(message.channel, embed=em)


###########################################
#                                         #
#          AUTOMATICS FUNCTIONS           #
#                                         #
###########################################
    if re.search(r'^(bonjour |salut |hello |bjr |slt |s\'lut)?([^ ]+ ){0,3}(qui s\'y conna(î|i)(t|s)|des gens|quelqu\'un|qqun|des personnes|du monde s\'y connait)[^\?]+\?$', message.content):
        await client.send_message(message.channel, ":question: N'hésite pas à poser ta question directement " + message.author.mention + ", il n'est pas utile de demander si quelqu'un connait quelque chose avant.")

    if message.content == message.content.upper() and not message.author.bot:
        if len(message.content) > 5:
            await client.send_message(message.channel, message.author.mention + " pas que des capitales dans ton message quand même !")
client.run(token)
