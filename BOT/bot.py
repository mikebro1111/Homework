import requests
import pandas as pd
import telebot

BOT_TOKEN = "1241924195:AAHn2F3xlV-6INaBkzg6wZRVRoPDn9H_P7o"  # ToDo: better secure

SUMMARY_URL = "https://api.covid19api.com/summary"

response = requests.get(SUMMARY_URL).json()

last_updated_date = response["Date"][:10]

global_df = pd.DataFrame({"In the whole world": response["Global"]})
global_df.index.name = last_updated_date
global_msg = "🌎 Global"

df = pd.DataFrame(response["Countries"]).set_index(["Country"])
df = df.loc[:, "NewConfirmed":"TotalRecovered"]

HELP_DICT = {
    "/start": "Start bot",
    "/countries_list": "Get list of available countries in button view",
    "/ua_map": "Get link to the map web view (Ukraine)",
    "/ua_regions": "Get stats for Ukraine grouped by region",
    "/help": "Get help info"
}

def update_ua_regions():
    ua_regions_df = pd.read_html(requests.get("https://tk.media/coronavirus").text)[0].iloc[1:]
    ua_regions_df.columns = ["Регіон"] + ua_regions_df.columns[1:].tolist()
    ua_regions_df.to_csv('data/ua_regions.csv')
    return ua_regions_df


bot = telebot.TeleBot(BOT_TOKEN)

empty_markup = telebot.types.ReplyKeyboardRemove(selective=False)

@bot.message_handler(commands=["start"])
def start(message):
    send_mess = f"<b>Hello {message.from_user.first_name}!</b>\n\nPlease, use /help to find more Functionality of this bot"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup, parse_mode="html")

@bot.message_handler(commands=["help"])
def help(message):
    send_mess = "\n".join([cmd + ' - ' + descr for cmd, descr in HELP_DICT.items()])
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup)

@bot.message_handler(commands=["countries_list"])
def countries_list(message):
    send_mess = "Choose a country:"
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row(telebot.types.KeyboardButton(global_msg))
    for country_name in df.index:
        itembtn = telebot.types.KeyboardButton(country_name)
        markup.row(itembtn)
    bot.send_message(message.chat.id, send_mess, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == global_msg)
def global_stats(message):
    send_mess = f"<b>{global_msg}</b>\n\n<pre>" + global_df.to_markdown() + "</pre>"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup, parse_mode="html")

@bot.message_handler(func=lambda message: message.text in df.index)
def country_stats(message):
    country_name = message.text
    tmp_df = df.loc[country_name].to_frame()
    tmp_df.index.name = last_updated_date
    send_mess = f"<b>{country_name}</b>\n\n<pre>" + tmp_df.to_markdown() + "</pre>"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup, parse_mode="html")

@bot.message_handler(commands=["ua_map"])
def ua_map(message):
    send_mess = "http://mikebro1111.pythonanywhere.com"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup)

@bot.message_handler(commands=["ua_regions"])
def ua_regions(message):
    ua_regions_df = update_ua_regions()
    send_mess = "<b>Статистика по Україні 🇺🇦</b>\n\n<pre>" + ua_regions_df.to_markdown() + "</pre>"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup, parse_mode="html")

@bot.message_handler(func=lambda message: True)
def others(message):
    send_mess = "Sorry, can't proceed your message/command\n\nPlease, use /help"
    bot.send_message(message.chat.id, send_mess, reply_markup=empty_markup)

bot.polling(none_stop=True)
