##################
#   Help & Info  #
# View Readme.md #
##################
__author__ = "Maël — outout14"
__licence__ = "Apache License 2.0"


##################
#   IMPORTS     #
#################
import discord ##Discord.py library
import asyncio
from config import * ##Configuration file
import random
import time
import sys
import math

client = discord.Client()


@client.event
async def on_ready():
    print("=-=-=-=-=-=-=")
    print("Radis" + version)
    print("Un bot discord par outout14")
    print(" ")
    print("Pret ! ")
    print("Vous pouvez l'utiliser.")
    await client.change_status(game=discord.Game(name=game), idle=False) ## Game set in config.py
    print("Jeu joué : " + game)
    print(client.user.name)
    print(client.user.id)
    print("=-=-=-=-=-=-=")


@client.event
async def on_message(message):
    if message.content.startswith(prefix + "afk"):##AFK
        msg = await client.send_message(message.channel, message.author.mention + " est désormais afk 🌚")
        await client.delete_message(message)

    elif message.content.startswith(prefix + "back"): ##AFK
        await client.send_message(message.channel, message.author.mention + " n'est plus afk 🌞")
        await client.delete_message(message)

    elif message.content.startswith(prefix + "coin"): ##PIECE
        piece = random.choice(["Pile", "Face", "... Heu, je l'ai perdu !"])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, "La piece est retombé sur " + piece)
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "joke"): ##Joke
        joke = random.choice(['Linux : lose your time\nMac : lose your money','Un virus est un programme nocif.\nIl est petit, rapide, prend peu de place en mémoire et sais se faire discret.\nOSX n\'est donc pas un virus, c\'est un bug.','Quel est le plus gros Apple du monde ? \n *Le big MAC...*','OSX est à l\'informatique ce que la tectonick est à la musique...','Si les OS étaient des élèves:\nOSX: Le plus vieux\nLinux: Le premier de la classe\nWindows: Le différent victimisé','Windows, Mac Os et Linux sont aux toilettes.  Mac OS se lave complètement les mains en sortant et déclare : Rien de plus sûr que ça ! Linux se lave uniquement deux doigts : Pas besoin de plus de sécurité ! Windows sort sans se laver les mains : Chez Windows, on ne s\'urine pas dessus !','https://cdn.discordapp.com/attachments/187284361505144833/187287424852951042/unknown.png !','Les hyperboles sa sert à manger des hyper-soupes :3 (Lawl!)','Attention : une étude récente a prouvé que la consommation prolongée de drogues peut définitivement endommager la mémoire à court terme.','https://images-1.discordapp.net/.eJwlyFEKhCAQANC7eAAn09TtNmJisTUjzkQf0d1bWHhf71Zn39WsVpHGM8Cycaa-aBbqqRZdiepeUttYZzogiaS8HgWFwcQwRme9mYbJOBet_VcwYbTB-8_wAyd-kS7UDat6XggYIuY.Tzl6-x2F39v_DjLRKkOBafZcvUg.png','C\'est un aveugle qui rentre dans un bar, qui rentre dans une chaise, qui rentre dans une table,..', 'Le comble de Windows, c’est que pour l’arrêter, il faut cliquer sur démarrer x)', 'C\'est un type qui rentre dans un bar et qui s\'exclame "Salut c\'est moi !", tout le monde se retourne, c\'était pas lui...', 'Que prend un éléphant dans un bar ? De la place...', 'Un zoophile prend son élan avant de rentrer dans un bar :D !', 'Pourquoi un aveugle vous tutoi ? Car il ne vous voit pas.....', 'C\'est une requête SQL qui rentre dans un bar et qui s\'adresse à deux tables : Puis-je vous joindre ?','Combien de développeurs faut-il pour remplacer une ampoule grillée ? Aucun, c\'est un problème Hardware.','4h du matin un homme rentre chez lui mort bourré. Pour ne pas se faire prendre par sa femme il decide de se faire un jus de citron. Le lendemain matin sa femme lui crie dessus. "Tu as encore bus comme un trou hier" L\'homme: "Mais non" La femme: "A ouais et le cannari dans le presse citron il s\'est suicider"']) #Source Bukkit.fr | https://www.bukkit.fr/topic/21638-recensement-de-blagues/
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + " " + joke)
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "ethylotest"): ##ALCHOL
        resultat = random.choice([" 🚔 😵 Vous avez trop bu !", " 🚔 🚙 Vous pouvez circuler.", " 🚔 Où ais-je mon ethylotest de !@#12è@56"])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + resultat)
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "clock france"): ##time
        await client.send_typing(message.channel)
        now = time.localtime(time.time())
        msg = await client.send_message(message.channel, message.author.mention + "🇲🇫 🕓 : Il est actuellement : " + time.strftime("%H:%M", now))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "clock canada"): ##time
        await client.send_typing(message.channel)
        now = time.localtime(time.time())
        Heure = time.strftime('%H')
        Heure = int(Heure)
        Heure -= 6
        Heure = str(Heure)
        print(Heure)
        msg = await client.send_message(message.channel, message.author.mention + "🇨🇦 🕓 : Il est actuellement : " + str(Heure) + ":" + time.strftime("%M", now))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "clock"): ##clock error
        msg = await client.send_message(message.channel, message.author.mention + "❌ __**[Erreur]**__ Usage: .clock france/canada")
        await asyncio.sleep(5)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "info"): ##info
        msg = await client.send_message(message.channel, message.author.mention + "🍁 **Radis bot INFO** \n⛪ **Développeur** : Outout14 \n**📰 Site** : https://radis.blackscarx.com/\n⚙ **Version** :" + version + " \n 🖥 Host : **Powered by BlackScarx**.\n 🔧 Api : **discord.py**\n ⌨ Langage : **Python**\n \n 📝 Prochainement : **Secret**\n 📪 Idées ? Envoyez moi un mail à **outout@blackscarx.com** !")
        await asyncio.sleep(20)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "yt discover"): ##chaines yt
        chaineyt = random.choice(['Les teachers du net, tutoriels | Lien : https://www.youtube.com/user/hounwanou1993','5secondfilms (Anglais), des courts-métrage | Lien : https://www.youtube.com/user/5secondfilms','TomSka (Anglais), des courts-métrages | Lien : https://www.youtube.com/user/TomSka','Trash, des Tops | Lien : https://www.youtube.com/channel/UCfGfdZuYifBYb1fmZcL1JBQ','ElectronikHeart, l\'informatique sous un angle différent | Lien : https://www.youtube.com/user/ElectronikHeart','Blender Foundation, des court-métrages réalisés avec Blender | Lien : https://www.youtube.com/channel/UCSMOQeBJ2RAnuFungnQOxLg','Caljbeut, politique, etc... en dessins | Lien : https://www.youtube.com/channel/UCNM-UkIP1BL5jv9ZrN5JMCA','SetSolution, des concepts d\'Iphones, etc... | Lien : https://www.youtube.com/channel/UCAXlQL_BcggjH6MpMSekjYg'])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + "🖥 [Youtube Discover] - Je peux te conseiller cette chaine youtube : " + chaineyt)
        await asyncio.sleep(20)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + "yt"): ##yt error
        msg = await client.send_message(message.channel, message.author.mention + "❌ __**[Erreur]**__ Commandes disponibles: 👉 .yt discover : Découvrir des chaînes youtubes !")
        await asyncio.sleep(5)
        await client.delete_message(msg)
        await client.delete_message(message)
##PHONE UPDATE
    elif message.content.startswith(prefix + 'phone send 3360 EX'): ##Phone
        await client.send_typing(message.channel)
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Votre Ex vous aime toujours ? La réponse est ' + str(reponse))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone send 3360 DAESH'): ##Phone
        await client.send_typing(message.channel)
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Allez vous être tué(e) lors d\'un attentat ? La réponse est ' + str(reponse))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone send 3360 BOMB'): ##Phone
        await client.send_typing(message.channel)
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Y\'a t-il une bombe allemande sous votre maison? La réponse est ' + str(reponse))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone send 3360 GUERRE'): ##Phone
        await client.send_typing(message.channel)
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Votre enfant va t-il se faire tuer lors de la 3eme guerre mondiale? La réponse est ' + str(reponse))
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone send 666'): ##Phone
        await client.send_typing(message.channel)
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 666 (Maintenant): 😡 Ce sera fait ! Je cherche mon fusil !')
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone send 2512'): ##Phone
        await client.send_typing(message.channel)
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 2512 (Maintenant): HoHoHo ! J\'ai bien reçu ta lettre ! ')
        await asyncio.sleep(10)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone list'): ##Phone
        await client.send_typing(message.channel)
        msg = await client.send_message(message.author, message.author.mention + '📱 📒 Liste des numéros\nPour envoyer un message à un de ces numéros; .phone send Numéro Message\n \n👤 3360 | Votre ex vous aime t-il toujours ? Envoyez EX au 3360 !\n👤 3360 | Allez vous être tué lors d\'un attentat ? Envoyez DAESH au 3360\n👤 3360 | Votre enfant va t-il se faire tuer lors de la 3eme guerre mondiale? Envoyez GUERRE au 3360\n👤 3360 | Y\'a t-il une bombe allemande sous votre maison? Envoyez BOMBE au 3360\n \n👤 2512 | Envoyez votre liste au père noël !\n👤 666 | Envoyer un message au **DIABLE** ! Pour tuer votre voisin, etc...')
        await asyncio.sleep(15)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone help'): ##Phone
        await client.send_typing(message.channel)
        msg = await client.send_message(message.author, message.author.mention + '🍁 Radis Bot - 📱 Commandes .phone\nℹ Liste des commandes : \n👉 .phone list : affiche les numéros existants.\n👉 .phone send <Numéro> <Message>, envoie un message à un numéro.\n👉 .phone help, Affiche l\'aide')
        await asyncio.sleep(20)
        await client.delete_message(msg)
        await client.delete_message(message)

    elif message.content.startswith(prefix + 'phone'): ##Phone
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + '❌ __**[Erreur]**__ Une erreur est survenue. Essayez .phone help')
        await asyncio.sleep(5)
        await client.delete_message(msg)
        await client.delete_message(message)

##END PHONE Update

##Start pokemon Update

##COMMANDES
    elif message.content.startswith(prefix + 'pokemon fight'): ##COMBAT
        await client.send_typing(message.channel)
        poke1 = random.choice(['Ratifeu','Squirtle','Ninetales','Bulbizarre','Carabaffe','Carapuce','Roucarnage','Nidorino','Akwakwak','Miaouss','Ratifeu','Squirtle','Ninetales','Bulbizarre','Carabaffe','Carapuce','Roucarnage','Nidorino','Akwakwak','Miaouss','outout14'])
        poke2 = random.choice(['Psyko','Arcanin','Boustiflor','Fantominus','Voltorbe','Excelangue','Poissirène','Magicarpe','Électhor','Joliflor','Cotovol','Mentali'])
        win = random.choice([str(poke1),str(poke2)])
        msg1 = await client.send_message(message.channel, '**Le combat Commence !**')
        msg2 = await client.send_message(message.channel, '📢 **Présentateur** : Les combatants sont : ' + str(poke1) + ' Contre ' + str(poke2))
        msg3 = await client.send_message(message.channel, '*Narateur : Le combat se déroule...*')
        await client.send_typing(message.channel)
        await asyncio.sleep(10)
        msg4 = await client.send_message(message.channel, '**📢 Présentateur** : Le gagnant est..... ')
        await client.send_typing(message.channel)
        await asyncio.sleep(1)
        msg5 = await client.send_message(message.channel, '**📢 Présentateur** : **' + str(win) + '**')
        await asyncio.sleep(30)
        await client.delete_message(msg1)
        await client.delete_message(msg2)
        await client.delete_message(msg3)
        await client.delete_message(msg4)
        await client.delete_message(msg5)
##Help & bugs
##If error :
    elif message.content.startswith(prefix + 'pokemon'): ##Pokemon error
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + '❌ __**[Erreur]**__ Une erreur est survenue....')
        await asyncio.sleep(5)
        await client.delete_message(msg)
##End pokemon Update


    elif message.content.startswith(prefix + 'help'): ##HELP
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel,'🍁 Radis Bot \nℹ Liste des commandes : \n \n📎 Diverses\n👉 .help, Afficher l\'aide.\n👉 .info, Affiche la version et d\'autres informations à propos de RadisBot\n👉 .phone help, Affiche l\'aide pour le téléphone\n \n🛠 Utilitaires\n👉 .afk, Signaler son absence. \n👉 .back, Signaler son retour. \n👉 .clock france/canada, Affiche l\'heure. \n👉 .yt discover , Découvrir des chaînes youtubes ! \n \n😂  Funs\n 👉 .joke, Affiche une blague aléatoirement.\n👉 .ethylotest, Avez vous bu ?\n 👉 .coin, Lance une pièce.\n 👉 .pokemon fight, Lance un combate contre deux pokémons *(aléatoirement)*.\n \n📱Téléphone (Visibles dans .phone help)\n👉 .phone list : affiche les numéros existants.\n👉 .phone send <Numéro> <Message>, envoie un message à un numéro.\n👉 .phone help, Affiche l\'aide\n \n')
        await asyncio.sleep(30)
        await client.delete_message(msg)
client.run(token)
