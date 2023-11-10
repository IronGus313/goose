import sqlite3
import random
import time
import requests
import json

import telebot
from telebot import types

bot = telebot.TeleBot('token')
name = ''
kid = None
kid1 = None

# API from https://openweathermap.org/
API = 'API key'

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('skibidi.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), chat_id INT)')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Enter your name')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    conn = sqlite3.connect('skibidi.sql')
    cur = conn.cursor()
    cur.execute(' SELECT * FROM users')
    users = cur.fetchall()
    chat_id = message.chat.id
    print(chat_id)

    for i inusers:
        global kid1
        if chat_id == i[2]:
            bot.send_message(message.chat.id, f'You have already registered under the name: {i[1]}')
            kid1 = True
            break
    if kid1:
        pass
    else:
        cur.execute('INSERT INTO users (name, chat_id) VALUES (?, ?)', (name, chat_id))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'type /help for instruction')

def send_message_to_user(user_name, message_text):
    conn = sqlite3.connect('skibidi.sql')
    cur = conn.cursor()

    cur.execute('SELECT chat_id FROM users WHERE name = ?', (user_name,))
    result = cur.fetchone()

    if result:
        user_chat_id = result[0]
        bot.send_message(user_chat_id, message_text)

    cur.close()
    conn.close()

@bot.message_handler(commands=['help'])
def help1(message):
    bot.send_message(message.chat.id,
                     f'/send_message : Send message to one of users\n/all_users : Shows all of the users\n\n/weather : Shows the weather in the city you selected')

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Enter the name of the city')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text.strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    data = json.loads(res.text)
    if 'main' in data:
        print(data["main"])
        temperature = int(data["main"]["temp"])
        bot.reply_to(message, f'The current weather is: {temperature} degrees Celsius')
    else:
        bot.reply_to(message, 'Unable to get weather data for the specified city. Perhaps the city was not found.')

@bot.message_handler(commands=['send_message'])
def pass11(message):
    bot.send_message(message.chat.id, "Enter the password")
    bot.register_next_step_handler(message, send_message_command)

def send_message_command(message):
    pass11 = message.text.strip()
    if pass11 == '4274':
        bot.send_message(message.chat.id, "Enter the username you want to send a message to:")
        bot.register_next_step_handler(message, send_message_to_username)
    else:
        bot.send_message(message.chat.id, 'Incorrect password')

def send_message_to_username(message):
    user_name = message.text.strip()

    conn = sqlite3.connect('skibidi.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for i inusers:
        global kid
        if i[1] == user_name:
            bot.send_message(message.chat.id, "Enter the message you want to send:")
            bot.register_next_step_handler(message, lambda msg: send_message_content(msg, user_name))
            kid = True
            break

    if kid:
        pass
    else:
        bot.send_message(message.chat.id, 'There is no such user')
    cur.close()
    conn.close()

def send_message_content(message, user_name):
    message_content = message.text.strip()

    conn = sqlite3.connect('skibidi.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    for i inusers:
        global kid
        if i[1] == user_name:
            send_message_to_user(user_name, message_content)
            bot.send_message(message.chat.id, f"The message has been successfully sent to the user {user_name}.")
            kid = True
            break

    if kid:
        pass
    else:
        bot.send_message(message.chat.id, 'There is no such user')
    cur.close()
    conn.close()

@bot.message_handler(commands=['all_users
