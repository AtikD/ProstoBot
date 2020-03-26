import telebot
from telebot import types
from pymongo import MongoClient
import os
import uuid
import random

client = MongoClient(os.environ["MongoDB"])
db = client.main
rulesColl = db.rules
adminsColl=db.admins
ruletkaColl=db.ruletka

uuidID = uuid.uuid1() 



bot=telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

bot.send_message(512177277, "Бот был перезапущен!")

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,"Привет! Подробно в /help")

@bot.message_handler(commands=['bezuzer'])
def bezUzera_message(message):	
	idd = message.text.split(' ')[1]
	bot.send_message(message.chat.id,f"[User](tg://user?id={idd})",parse_mode = "markdown")

@bot.message_handler(commands=['ktoya'])
def kto_Ya(message):
	ktoya=['Квантовый бомж','Квантовый компьютер', 'Сверх-мощный придурок']
	bot.send_message(message.chat.id,f"Вы {random.choice(ktoya)}!")

@bot.message_handler(commands=['help'])
def help_message(message):
  bot.send_message(message.chat.id,"Команды:\n/rules - Правила чата.\n/adminshelp - Команды для админов чата.")

@bot.message_handler(commands=['adminshelp'])
def admins_command(message):
	user = bot.get_chat_member(message.chat.id, message.from_user.id)
	if user.status == 'creator' or user.status == 'administrator':
		bot.send_message(message.chat.id,"Команды для админов:\n/newrules - Новые правила чата(Отвечать на чье-либо сообщение).\n/pin - Закрепить сообщение(Отвечать на чье-либо сообщение).\n/unpin - Открепить сообщение")
	else:
		bot.send_message(message.chat.id,"Вы не администратор чата!")

@bot.message_handler(commands=['infoc'])
def chatInfo(message):
  bot.send_message(message.chat.id,F"Айди чата: {message.chat.id}")

@bot.message_handler(commands=['randomnumber'])
def randomNumber(message):
	if message.text.split(' ')==[1]:	
		if message.text.split(' ')==[2]:
			num1=message.text.split(' ')[1]
			num2=message.text.split(' ')[2]
			randn1=random.randint(num1,num2)
			bot.send_message(message.chat.id,F"{randn1}")
		else:
			bot.send_message(message.chat.id,"/randomnumber {число1} {число2}")
	else:	
		randn2=random.randint(0,100)
		bot.send_message(message.chat.id,F"{randn2}")

@bot.message_handler(commands=['pin'])
def PinMessage(message):
	if message.reply_to_message!=None:
		user = bot.get_chat_member(message.chat.id, message.from_user.id)
		print(user)
		if user.status == 'creator' or user.status == 'administrator':
			bot.pin_chat_message(message.chat.id,message.reply_to_message.message_id)
			bot.send_message(message.chat.id,"Успешно выполнено!")
		else:
			bot.send_message(message.chat.id,"Вы не администратор!")
	else:
		bot.send_message(message.chat.id,"Ответьте на сообщение.")
		
@bot.message_handler(commands=['unpin'])
def unPinMessage(message):
	user = bot.get_chat_member(message.chat.id, message.from_user.id)
	if user.status == 'creator' or user.status == 'administrator':
		bot.unpin_chat_message(message.chat.id)
		bot.send_message(message.chat.id,"Успешно выполнено!")
	else:
		bot.send_message(message.chat.id,"Вы не администратор чата!")

@bot.message_handler(commands=['infou'])
def userInfo(message):
	if message.reply_to_message!=None:
		bot.send_message(message.chat.id,f"Он [{message.reply_to_message.from_user.first_name}](tg://user?id={message.reply_to_message.from_user.id})\nЕго айди: {message.reply_to_message.from_user.id}",parse_mode = "markdown")
	else:
		bot.send_message(message.chat.id,f"Вы [{message.from_user.first_name}](tg://user?id={message.from_user.id})\nВаш айди: {message.from_user.id}" ,parse_mode = "markdown")

@bot.message_handler(commands=['infom'])
def messageInfo(message):
	if message.reply_to_message!=None:
		bot.send_message(message.chat.id,f"Айди сообщения: {message.reply_to_message.message_id}\nКто его писал: [message.reply_to_message.from_user.first_name](tg://user?id={message.reply_to_message.from_user.id})",parse_mode = "markdown")
	else:
		bot.send_message(message.chat.id,"Отвечайте на чье-либо сообщение!")
	
@bot.message_handler(commands=['rules'])
def rules(message):
	chatId=rulesColl.find_one({"chatid": message.chat.id})
	if message.chat.id==chatId:
		rulesid=rulesColl.find_one({"rules": message.chat.id})
		rulesChatOtId=rulesColl.find_one({"otchatid": {'$exists': True}})
		bot.forward_message(message.chat.id,f"{rulesChatOtId['otchatid']}",f"{rulesid['rules']}")

@bot.message_handler(commands=['newrules'])
def newrules(message):
	if message.reply_to_message!=None:
		user = bot.get_chat_member(message.chat.id, message.from_user.id)										
		if user.status == 'creator' or user.status == 'administrator':
			deleterules = rulesColl.delete_many ({})
			newrules = { "rules": message.reply_to_message.message_id,"otchatid":message.chat.id,"chatid":message.chat.id}
			rulesColl.insert_one(newrules)
			bot.send_message(message.chat.id,"Правила установлены!")	
		else:
			bot.send_message(message.chat.id,"Вы не администратор чата!")

bot.polling(none_stop=True)
