##################
#   Help & Info  #
# View Readme.md #
##################
__author__ = "Maël — outout"
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
import os
import urllib 
import urllib.request ##URL functions

client = discord.Client()
staetus = "dnd"

@client.event
async def on_ready():
    print("=-=-=-=-=-=-=")
    print("TuxBot" + version)
    print("Ready ! ")
    print("Vous pouvez l'utiliser.")
    await client.change_presence(game=discord.Game(name=game), status=discord.Status(staetus), afk=False) ## Game set in config.py
    print("Jeu joué : " + game)
    print("Pseudo du bot : " + client.user.name)
    print("UserID du bot : " + client.user.id)
    print("=-=-=-=-=-=-=")

@client.event
async def on_message(message):
    
    roles = ["admin", "Admin", "ADMIN"]
    role = message.author.roles

    if message.content.startswith(prefix + "debug ping") and str(role[1]) in roles:
        msg = await client.send_message(message.channel, message.author.mention + "[**Debug**] : Bot online !")

    elif message.content.startswith(prefix + "say") and str(role[1]) in roles: ##CONTROL
      print("[Debug] Say command sended")
      args_ = message.content.split("(")
      argument = args_[1]
      await client.send_message(message.channel, args_[1])
      await client.delete_message(message)

    elif message.content.startswith(prefix + 'clear') and str(role[1]) in roles:
        args = message.content.split(" ")
        argument = int(args[1])
        argument = argument+1
        deleted = await client.purge_from(message.channel, limit=argument)
        msg = await client.send_message(message.channel, message.author.mention + " les messages ont bien été supprimés")

    elif message.content.startswith(prefix + 'changegame') and str(role[1]) in roles:
        args = message.content.split("(")
        argument = args[1]
        await client.change_presence(game=discord.Game(name=args[1]), status=discord.Status(staetus), afk=False) ## Game set in config.py
        msg = await client.send_message(message.channel, message.author.mention + " le jeu à bien été modifié !")

    elif message.content.startswith(prefix + 'search docubuntu'):
        args_ = message.content.split(" ")
        argument = args_[1]
        await client.send_typing(message.channel)
        await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de parcourir le WorldWideWeb, et ça peut prendre du temps ! ")
        await client.send_typing(message.channel)
        html = urllib.request.urlopen("https://doc.ubuntu-fr.org/" + args_[2]).read()
        await client.send_typing(message.channel)
        if "avez suivi un lien" in str(html):
            await client.send_message(message.channel, message.author.mention + " :sob: Oh non ! Cette page n'existe pas sur la doc ubuntu-fr. Vous pouvez commencer à la rédiger ! https://doc.ubuntu-fr.org/"+ args_[2])
        else:
            await client.send_message(message.channel, message.author.mention + " :ok_hand: Trouvé ! Voici la page ramenant à votre recherche https://doc.ubuntu-fr.org/"+ args_[2])

    elif message.content.startswith(prefix + 'search wikileaks'):
        args_ = message.content.split(" ")
        argument = args_[1]
        await client.send_typing(message.channel)
        await client.send_message(message.channel, message.author.mention + " **Veuillez patienter**, Je suis entrain de parcourir le WorldWideWeb, et ça peut prendre du temps ! ")
        await client.send_typing(message.channel)
        html = urllib.request.urlopen("https://search.wikileaks.org/?query=" + args_[2] + "#results").read()
        await client.send_typing(message.channel)
        if "0 results" in str(html):
            await client.send_message(message.channel, message.author.mention + " :sob: Oh non ! Aucun élément ne correspond de pres ou de loin a votre recherche.")
        else:
            await client.send_message(message.channel, message.author.mention + " :ok_hand: Trouvé ! Le résultat de votre recherche est ici => https://search.wikileaks.org/?query=" + args_[2] + "#results")

    elif message.content.startswith(prefix + 'search'):
        await client.send_typing(message.channel)
        await client.send_message(message.channel, message.author.mention + " TuxBot - :mag: Commandes .search\n \n Attention ! : entrez vos termes de recherche sans espaces ! \n  \n :information_source: Liste des commandes : \n **Wikileaks** : .search wikileaks _terme de la recherche_ \n **Doc.ubuntu-fr.org** : .search docubuntu _terme de la recherche_")

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

    elif message.content.startswith(prefix + "joke"): ##Joke
        joke = random.choice(['C\'est possible d\'installer i3 sur un processeur AMD ?','Linux : lose your time\nMac : lose your money','Un virus est un programme nocif.\nIl est petit, rapide, prend peu de place en mémoire et sais se faire discret.\nOSX n\'est donc pas un virus, c\'est un bug.','Quel est le plus gros Apple du monde ? \n *Le big MAC...*','OSX est à l\'informatique ce que la tectonick est à la musique...','Si les OS étaient des élèves:\nOSX: Le plus vieux\nLinux: Le premier de la classe\nWindows: Le différent victimisé','Windows, Mac Os et Linux sont aux toilettes.  Mac OS se lave complètement les mains en sortant et déclare : Rien de plus sûr que ça ! Linux se lave uniquement deux doigts : Pas besoin de plus de sécurité ! Windows sort sans se laver les mains : Chez Windows, on ne s\'urine pas dessus !','https://cdn.discordapp.com/attachments/187284361505144833/187287424852951042/unknown.png !','Les hyperboles sa sert à manger des hyper-soupes :3 (Lawl!)','Attention : une étude récente a prouvé que la consommation prolongée de drogues peut définitivement endommager la mémoire à court terme.','https://images-1.discordapp.net/.eJwlyFEKhCAQANC7eAAn09TtNmJisTUjzkQf0d1bWHhf71Zn39WsVpHGM8Cycaa-aBbqqRZdiepeUttYZzogiaS8HgWFwcQwRme9mYbJOBet_VcwYbTB-8_wAyd-kS7UDat6XggYIuY.Tzl6-x2F39v_DjLRKkOBafZcvUg.png','C\'est un aveugle qui rentre dans un bar, qui rentre dans une chaise, qui rentre dans une table,..', 'Le comble de Windows, c’est que pour l’arrêter, il faut cliquer sur démarrer x)', 'C\'est un type qui rentre dans un bar et qui s\'exclame "Salut c\'est moi !", tout le monde se retourne, c\'était pas lui...', 'Que prend un éléphant dans un bar ? De la place...', 'Un zoophile prend son élan avant de rentrer dans un bar :D !', 'Pourquoi un aveugle vous tutoi ? Car il ne vous voit pas.....', 'C\'est une requête SQL qui rentre dans un bar et qui s\'adresse à deux tables : Puis-je vous joindre ?','Combien de développeurs faut-il pour remplacer une ampoule grillée ? Aucun, c\'est un problème Hardware.','4h du matin un homme rentre chez lui mort bourré. Pour ne pas se faire prendre par sa femme il decide de se faire un jus de citron. Le lendemain matin sa femme lui crie dessus. "Tu as encore bus comme un trou hier" L\'homme: "Mais non" La femme: "A ouais et le cannari dans le presse citron il s\'est suicider"', 'Il ne faut jamais croire les girafes, c\'est un cou monté.', 'Quelle est la seule fonctionnalité qui n\'as jamais planté sur Windows ? Le BSOD', 'Windows n\'aime pas quel l\'on appel un dossier con, car c\'est le synonyme de son créateur (Gaston Portail)', 'Pourquoi personne n\'aime ISS? Car il était utilisé par les NAZIS', 'Sous Mac il n\'y a qu\'un virus : MacOSX', 'Le meilleur entreprise de système d\'exploitation ? Apple : Ils exploitent ton argent', 'Windows est un OS. Il est dur, n\'as pas de goût et on veut l\'enterrer']) #Source Bukkit.fr | https://www.bukkit.fr/topic/21638-recensement-de-blagues/
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + " " + joke)

    elif message.content.startswith(prefix + "ethylotest"): ##ALCHOL
        resultat = random.choice([" 🚔 😵 Vous avez trop bu !", " 🚔 🚙 Vous pouvez circuler.", " 🚔 Où ais-je mon ethylotest de !@#12è@56"])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + resultat)

    elif message.content.startswith(prefix + "clock canada"): ##time
        await client.send_typing(message.channel)
        now = time.localtime(time.time())
        Heure = time.strftime('%H')
        Heure = int(Heure)
        Heure -= 1
        Heure = str(Heure)
        print(Heure)
        msg = await client.send_message(message.channel, message.author.mention + "🇨🇦 🕓 : Il est actuellement : " + str(Heure) + ":" + time.strftime("%M", now))

    elif message.content.startswith(prefix + "clock france"): ##time
        await client.send_typing(message.channel)
        now = time.localtime(time.time())
        Heure = time.strftime('%H')
        Heure = int(Heure)
        Heure += 5
        Heure = str(Heure)
        print(Heure)
        msg = await client.send_message(message.channel, message.author.mention + ":flag_fr: 🕓 : Il est actuellement : " + str(Heure) + ":" + time.strftime("%M", now))

    elif message.content.startswith(prefix + "clock suisse"): ##time
        await client.send_typing(message.channel)
        now = time.localtime(time.time())
        Heure = time.strftime('%H')
        Heure = int(Heure)
        Heure += 5
        Heure = str(Heure)
        print(Heure)
        msg = await client.send_message(message.channel, message.author.mention + ":flag_ch: 🕓 : Il est actuellement : " + str(Heure) + ":" + time.strftime("%M", now))

	
    elif message.content.startswith(prefix + "clock"): ##clock error
        msg = await client.send_message(message.channel, message.author.mention + "❌ __**[Erreur]**__ Usage: .clock france/canada/suisse")

    elif message.content.startswith(prefix + "info"): ##info
        msg = await client.send_message(message.channel, message.author.mention + "**TuxBot INFO** \n⛪ **Développeur** : Outout \n**📰 Site du dev'** : https://outout.tech/\n⚙ **Version** : 2" " \n 🖥 Host : **RaspberryPi 3 Type B**.\n 🔧 Api : **discord.py**\n ⌨ Langage : **Python**\n 📪 Idées ? Envoyez moi un mail à **outout@linuxmail.org** !")

    elif message.content.startswith(prefix + "ytdiscover"): ##chaines yt
        chaineyt = random.choice(['KickSama, dessins annimés : https://www.youtube.com/user/TheKickGuy', 'U=RI, videos sur l\'électricité | Lien : https://www.youtube.com/channel/UCVqx3vXNghSqUcVg2nmegYA', 'Outout, chaine de merde et peu alimenté du créateur du bot | Lien : https://www.youtube.com/channel/UC2XpYyT5X5tq9UQpXdc1JaQ', 'SuperJDay64, LP sur des jeux de type mario | Lien : https://www.youtube.com/channel/UCjkQgODdmhR9I2TatJZtGSQ/about', 'Monsieur Plouf, critiques de jeux AAA | Lien : https://www.youtube.com/channel/UCrt_PUTF9LdJyuDfXweHwuQ', 'MaxEstLa, vidéos réaction sur d\'autres chaines (c\'est presque du clash :D ) | Lien : https://www.youtube.com/channel/UCJFGk2A34R-99RIVDK2Hlwg', 'BastienLePirate, astuces youtube, vidéos sur des ytubers, ...| Lien : https://www.youtube.com/channel/UCJFGk2A34R-99RIVDK2Hlwg', 'Blender Foundation, animations libre de droits réalisé en utilisant blender | Lien : https://www.youtube.com/channel/UCSMOQeBJ2RAnuFungnQOxLg', 'Met-Hardware, chaine youtube sur l\'hardware et des let\'s play ! Lien : https://www.youtube.com/channel/UC7rse81OttysA1m1yn_f-OA', 'Les teachers du net, tutoriels | Lien : https://www.youtube.com/user/hounwanou1993','5secondfilms (Anglais), des courts-métrage | Lien : https://www.youtube.com/user/5secondfilms','TomSka (Anglais), des courts-métrages | Lien : https://www.youtube.com/user/TomSka','Trash, des Tops | Lien : https://www.youtube.com/channel/UCfGfdZuYifBYb1fmZcL1JBQ','ElectronikHeart, l\'informatique sous un angle différent | Lien : https://www.youtube.com/user/ElectronikHeart','Blender Foundation, des court-métrages réalisés avec Blender | Lien : https://www.youtube.com/channel/UCSMOQeBJ2RAnuFungnQOxLg','Caljbeut, politique, etc... en dessins | Lien : https://www.youtube.com/channel/UCNM-UkIP1BL5jv9ZrN5JMCA','SetSolution, des concepts d\'Iphones, etc... | Lien : https://www.youtube.com/channel/UCAXlQL_BcggjH6MpMSekjYg'])
        await client.send_typing(message.channel)
        msg = await client.send_message(message.channel, message.author.mention + "🖥 [Youtube Discover] - Je peux te conseiller cette chaine youtube : " + chaineyt)

    elif message.content.startswith(prefix + "yt"): ##yt error
        msg = await client.send_message(message.channel, message.author.mention + "❌ __**[Erreur]**__ Commandes disponibles: 👉 .yt discover : Découvrir des chaînes youtubes !")

    elif message.content.startswith(prefix + 'phone send 3360 EX'): ##Phone
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Votre Ex vous aime toujours ? La réponse est ' + str(reponse))

    elif message.content.startswith(prefix + 'phone send 3360 DAESH'): ##Phone
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Allez vous être tué(e) lors d\'un attentat ? La réponse est ' + str(reponse))

    elif message.content.startswith(prefix + 'phone send 3360 BOMB'): ##Phone
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Y\'a t-il une bombe allemande sous votre maison? La réponse est ' + str(reponse))

    elif message.content.startswith(prefix + 'phone send 3360 GUERRE'): ##Phone
        reponse = random.choice(['oui','non','oui','non'])
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Votre enfant va t-il se faire tuer lors de la 3eme guerre mondiale? La réponse est ' + str(reponse))

    elif message.content.startswith(prefix + 'phone send 666'): ##Phone
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 666 (Maintenant): 😡 Ce sera fait ! Je cherche mon fusil !')

    elif message.content.startswith(prefix + 'phone send 3360 BESTOS'): ##Phone
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 3360 (Maintenant): Les Systèmes GNU/Linux sont évidement les meilleurs !')

    elif message.content.startswith(prefix + 'phone send 2512'): ##Phone
        msg = await client.send_message(message.author, message.author.mention + 'ℹ Vous avez un nouveau message !\nLe 2512 (Maintenant): HoHoHo ! J\'ai bien reçu ta lettre ! ')

    elif message.content.startswith(prefix + 'phone list'): ##Phone
        msg = await client.send_message(message.author, message.author.mention + '📱 📒 Liste des numéros\nPour envoyer un message à un de ces numéros; .phone send Numéro Message\n \n👤 3360 | Votre ex vous aime t-il toujours ? Envoyez EX au 3360 !\n👤 3360 | Allez vous être tué lors d\'un attentat ? Envoyez DAESH au 3360\n👤 3360 | Votre enfant va t-il se faire tuer lors de la 3eme guerre mondiale? Envoyez GUERRE au 3360\n👤 3360 | Y\'a t-il une bombe allemande sous votre maison? Envoyez BOMBE au 3360\n \n👤 2512 | Envoyez votre liste au père noël !\n👤 666 | Envoyer un message au **DIABLE** ! Pour tuer votre voisin, etc...\👤 3360 | Quel est le meilleur système d\'exploitation ? Envoie BESTOS au 3360 !')

    elif message.content.startswith(prefix + 'phone help'): ##Phone
        await client.send_message(message.author, message.author.mention + 'TuxBot - 📱 Commandes .phone\nℹ Liste des commandes : \n👉 .phone list : affiche les numéros existants.\n👉 .phone send <Numéro> <Message>, envoie un message à un numéro.\n👉 .phone help, Affiche l\'aide')

    elif message.content.startswith(prefix + 'phone'): ##Phone
        await client.send_message(message.channel, message.author.mention + '❌ __**[Erreur]**__ Une erreur est survenue. Essayez .phone help')

    elif(message.content.startswith(prefix + 'pokemon')): ##COMBAT
        await client.send_typing(message.channel)
        poke1 = random.choice(['Tux','Ratifeu','Squirtle','Ninetales','Bulbizarre','Carabaffe','Carapuce','Roucarnage','Nidorino','Akwakwak','Miaouss','Ratifeu','Squirtle','Ninetales','Bulbizarre','Carabaffe','Carapuce','Roucarnage','Nidorino','Akwakwak','Miaouss','outout14'])
        poke2 = random.choice(['Psyko','Arcanin','Boustiflor','Fantominus','Voltorbe','Excelangue','Poissirène','Magicarpe','Électhor','Joliflor','Cotovol','Mentali'])
        if(poke1 == "Tux"):
            win = "Tux"
        else:
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


    elif message.content.startswith(prefix + 'help'): ##HELP
        await client.send_typing(message.channel)
        await client.send_message(message.channel,'TuxBot \nℹ Liste des commandes : \n \n📎 Diverses\n👉 .help, Afficher l\'aide.\n👉 .info, Affiche la version et d\'autres informations à propos de TuxBot\n👉 .phone help, Affiche l\'aide pour le téléphone\n👉 .github, Lien vers le github de TuxBot pour voir son code source \n \n🛠 Utilitaires\n👉 .afk, Signaler son absence. \n👉 .back, Signaler son retour. \n👉 .clock france/canada/suisse, Affiche l\'heure. \n👉 .ytdiscover , Découvrir des chaînes youtubes ! \n👉 .search, faire une recherche sur le WorldWideWeb \n \n😂  Funs\n👉 .joke, Affiche une blague aléatoirement.\n👉 .ethylotest, Avez vous bu ?\n 👉 .coin, Lance une pièce.\n 👉 .pokemon, Lance un combate contre deux pokémons *(aléatoirement)*.\n \n📱Téléphone (Visibles dans .phone help)\n👉 .phone list : affiche les numéros existants.\n👉 .phone send <Numéro> <Message>, envoie un message à un numéro.\n👉 .phone help, Affiche l\'aide\n \n')
        
        if str(role[1]) in roles: ##IF ADMINISTRATOR
            await client.send_message(message.channel, ':eye: Administration (requiert grade ADMIN)\n👉 .say(_votre message_) (avec les paranthèses) : Fait le bot parler \n👉 .clear _nombre_ : Vide _nombre_ de messages \n👉 .debug ping : Test si le bot est en ligne et à la permission d\'écrire. \n👉 .changegame(_votre texte_) (avec les paranthèses): Change le jeu joué par TuxBot ')

    elif message.content.startswith(prefix + 'github'): ##Link to github
        await client.send_typing(message.channel)
        await client.send_message(message.channel, message.author.mention + 'Oh c\'est sympa ! Tu veux aller voir mon code source sur Github ! :kissing_smiling_eyes: =>  https://github.com/outout14/tuxbot-bot')
client.run(token)
