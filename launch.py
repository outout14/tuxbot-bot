#! /usr/bin/env python3

import locale
from dialog import Dialog
from subprocess import call
import os 

locale.setlocale(locale.LC_ALL, '')
d = Dialog(dialog="dialog")
d.set_background_title("Tuxbot Manager v0.5a")

while True:

	mmenu, rmenu = d.menu("Que souhaitez vous faire ?", choices = [("(1)", "Lancer Tuxbot"), ("(2)", "Eteindre Tuxbot"), ("(3)", "Mettre à jour Tuxbot"), ("(4)", "Quitter")])
	
	if rmenu == "(1)":
		d.gauge_start("Lancement")
		d.gauge_update(10)
#		try:
#			call(["screen", "-S", "tuxbot", "-X","quit"])
#		except:
#			d.gauge_update(35)
		d.gauge_update(40)
		call(["screen","-S","tuxbot", "-d", "-m", "python3", "bot.py"])
		d.gauge_update(100)
		d.gauge_stop()
		d.msgbox("Tuxbot est correctement lancé ! Merci de faire .ping sur discord pour vérifier.")

	if rmenu == "(2)": 
		d.gauge_start("Arrêt")
		d.gauge_update(10)
		call(["screen", "-S", "tuxbot", "-X","quit"])
		d.gauge_update(100)
		d.gauge_stop()
		d.msgbox("Tuxbot s'est correctement arrêté. Faites vite ;-) !")

	if rmenu == "(4)":
		d.pause("A bientôt !\n(C) 2018 Gnous.EU Dev Team.", seconds=2)
		call(["clear"])
		exit()
		
	if rmenu == "(3)":
		d.msgbox("Fonctionnalité indisponible pour le moment du fait que le serveur GIT de tuxbot est hors service.") 
