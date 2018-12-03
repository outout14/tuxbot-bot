from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from .checks import check_date
import aiohttp, imghdr, textwrap, math, datetime

async def generate_passport(self, user, theme: str = None):
	name = user.name
	userid = user.id
	avatar = user.avatar_url
	def_avatar = user.default_avatar_url
	created = datetime.datetime.fromisoformat(str(user.created_at))
	nick = user.display_name
	discr = user.discriminator
	roles = user.roles

	top_role_color = str(user.top_role.color)[1:]
	user_color = tuple(int(top_role_color[i:i+2], 16) for i in (0, 2 ,4))
	user_color += (255,)

	color = {
		"dark": {
			"background": 39,
			"question": 220,
			"answer": 150
		},
		"light": {
			"background": 216,
			"question": 35,
			"answer": 61
		}
	}
	
	user_birth_day = check_date(str(created.day))
	user_birth_month = check_date(str(created.month))

	formated_user_birth = str(user_birth_day) + "/" + str(user_birth_month) + "/" + str(created.year)
	formated_passportdate = "n/a"

	roleImages = {}

	def draw_underlined_text(draw, pos, text, font, **options):
		twidth, theight = draw.textsize(text, font=font)
		lx, ly = pos[0], pos[1] + theight
		draw.text(pos, text, font=font, **options)
		draw.line((lx, ly, lx + twidth, ly), **options)

	def break_line(draw, pos, text, font, **options):
		lines = text.split("\n")
		current_y = pos[1]
		for line in lines:
			twidth, theight = draw.textsize(line, font=font)
			lx, ly = pos[0], current_y
			if textwrap.fill(line, 60) == line:
				draw.text((lx, ly), textwrap.fill(line, 60), font=font, **options)
				current_y += math.floor(theight)
			else: 
				draw.text((lx, ly), textwrap.fill(line, 60), font=font, **options)
				current_y += math.floor(theight*2)

	for x, role in enumerate(roles):
		try:
			roleImages[role.name] = Image.open(f"data/images/roles/small/{role.name.lower().replace(' user', '')}.png")
		except Exception as e:
			next

	if avatar == '':
		async with aiohttp.ClientSession() as session:
			async with session.get(def_avatar) as r:
				image = await r.content.read()
	else:
		async with aiohttp.ClientSession() as session:
			async with session.get(avatar) as r:
				image = await r.content.read()
	with open('data/users/avatars/{}.png'.format(user.id), 'wb') as f:
		f.write(image)
	
	checked = False

	while checked == False:
		checks = 0
		isImage = imghdr.what('data/users/avatars/{}.png'.format(user.id))

		if checks > 4:
			checked = True
		
		if isImage != 'None':
			checked = True
		else:
			checks += 1
	
	av = Image.open('data/users/avatars/{}.png'.format(user.id))
	userAvatar = av.resize((128, 128), resample=Image.BILINEAR).convert('RGBA')
	maxsize = ( 800, 500)
	try:
		bg = Image.open('data/users/backgrounds/{0}.png'.format(user.id))
		bg_width, bg_height = bg.size

		bg = ImageOps.fit(bg,maxsize)

	except:
		bg = Image.open('data/images/background_default.png')

	fontFace = 'data/fonts/{}'.format(self.bot.config.fonts['normal'])
	fontFace_bold = 'data/fonts/{}'.format(self.bot.config.fonts['bold'])

	fontSize = 18
	fontSizeVeryTiny = 16

	descSizeQuestion = 10
	descSizeAnswer = 10

	headerSize = 32
	headerSizeTiny = 24
	headerSizeVeryTiny = 16

	header_font = ImageFont.truetype(fontFace_bold, headerSize)
	header_font_tiny = ImageFont.truetype(fontFace_bold, headerSizeTiny)
	header_font_very_tiny = ImageFont.truetype(fontFace_bold, headerSizeVeryTiny)

	font = ImageFont.truetype(fontFace, fontSize)
	font_very_tiny = ImageFont.truetype(fontFace, fontSizeVeryTiny)

	desc_font_question = ImageFont.truetype(fontFace_bold, descSizeQuestion)
	desc_font_answer = ImageFont.truetype(fontFace, descSizeAnswer)
	font_bold = font = ImageFont.truetype(fontFace_bold, fontSize)

	answers = None

	self.cursor.execute("SELECT os, config, languages, pays, passportdate, theme FROM passport WHERE userid=%s", str(user.id))
	answers = self.cursor.fetchone()

	if not theme:
		if answers:
			theme = str(answers[5])
		else:
			theme = "dark"

	cardbg = Image.new('RGBA', (800, 500), (0, 0, 0, 255))
	d = ImageDraw.Draw(cardbg)

	d.rectangle([(0, 0), 800, 500], fill=(255, 255, 255, 255))
	cardbg.paste(bg, (0, 0))

	cardfg = Image.new('RGBA', (800, 500), (255, 255, 255, 0))
	dd = ImageDraw.Draw(cardfg)

	# Info Box Top
	dd.rectangle([(60, 60), (600, 191)], fill=(color[theme]["background"], color[theme]["background"], color[theme]["background"], 200))
	dd.rectangle([(60, 60), (600, 134)], fill=(color[theme]["background"], color[theme]["background"], color[theme]["background"], 255))

	# Avatar box
	if user_color == (0, 0, 0, 255):
		user_color = (color[theme]["background"], color[theme]["background"], color[theme]["background"], 255)
	dd.rectangle([(609, 60), (740, 191)], fill=user_color)
	cardfg.paste(userAvatar, (611, 62))

	# Profile Information
	if textwrap.fill(nick, 25) != nick:
		dd.text((70, 70), nick, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 220), font=header_font_very_tiny)
		dd.text((70, 106), '@' + name + '#' + discr, fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 225), font=font_very_tiny)
	elif textwrap.fill(nick, 15) != nick:
		dd.text((70, 70), nick, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 220), font=header_font_tiny)
		dd.text((70, 106), '@' + name + '#' + discr, fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 225), font=font)
	else:
		dd.text((70, 64), nick, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 220), font=header_font)
		dd.text((70, 106), '@' + name + '#' + discr, fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 225), font=font)

	draw_underlined_text(dd, (380, 75), "Date de parution sur discord :", fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 220), font=desc_font_question)
	dd.text((542, 75), formated_user_birth, fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 225), font=desc_font_answer)

	# Roles
	for idy, ii in enumerate(roleImages):

		startx = int((270 - (30 * len(roleImages))) / 2)

		cardfg.paste(roleImages[ii], (197 + startx + (30 * idy),152), roleImages[ii])


	#Info Box Bottom
	dd.rectangle([(60, 200), (740, 450)], fill=(color[theme]["background"], color[theme]["background"], color[theme]["background"], 200))

	if answers:
		passportdate = datetime.datetime.fromisoformat(answers[4])
		passportdate_day = check_date(str(passportdate.day))
		passportdate_month = check_date(str(passportdate.month))

		formated_passportdate = str(passportdate_day) + "/" + str(passportdate_month) + "/" + str(passportdate.year)

		draw_underlined_text(dd, (80, 220), "Système(s) d'exploitation :", desc_font_question, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 255))
		break_line(
			dd,
			(80, 240), 
			answers[0],
			fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 255), 
			font=desc_font_answer
		)

		draw_underlined_text(dd, (80, 300), "Langages de programmation préférés :", desc_font_question, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 255))
		break_line(
			dd,
			(80, 320), 
			answers[2],
			fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 255), 
			font=desc_font_answer
		)

		draw_underlined_text(dd, (80, 380), "Pays :", desc_font_question, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 255))
		break_line(
			dd,
			(80, 400), 
			answers[3],
			fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 255), 
			font=desc_font_answer
		)

		dd.line((400, 220, 400, 430), fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 255))

		draw_underlined_text(dd, (410, 220), "Configuration Système :", desc_font_question, fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 255))
		break_line(
			dd,
			(410, 240), 
			answers[1],
			fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 255), 
			font=desc_font_answer
		)

	else:
		dd.text(
			(370, 300),
			"Non renseigné.", 
			fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 255),
			font=desc_font_question
		)

	draw_underlined_text(dd, (380, 100), "Date de création du passeport :", fill=(color[theme]["question"], color[theme]["question"], color[theme]["question"], 220), font=desc_font_question)
	dd.text((542, 100), formated_passportdate, fill=(color[theme]["answer"], color[theme]["answer"], color[theme]["answer"], 225), font=desc_font_answer)

	card = Image.new('RGBA', (800, 500), (255, 255, 255, 255))
	card = Image.alpha_composite(card, cardbg)
	card = Image.alpha_composite(card, cardfg)

	return card