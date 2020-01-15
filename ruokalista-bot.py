# access token: 926759597:AAHxu95K0wEexYYOqATOyNpGV6STZkN5gLU
# remove before github!!!!

import logging
import time
import os
import sys
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import json
import requests

""" TODO ominaisuudet
    - Päivän menun tulostaminen sekä muotoilu
    - Menun lähettäminen telegram kanavalle
    - Lisätä loput ravintolat
    - Päivän menun automaattinen lähettäminen aina klo 11
    - Ehkä: Ruokalistan lähettäminen sijainnin mukaan
    TODO koodi
    - Selkeät aliohjelmat
    - Kommentointi
    - Virhekäsittely
"""
token = '926759597:AAHxu95K0wEexYYOqATOyNpGV6STZkN5gLU'

#logging
logging.basicConfig(format='%(astime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger()


#mode switch
mode = "dev"#os.getenv("MODE")
TOKEN = token#os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
        updater.idle()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)



# Haetaan webistä ruokalista ja tulostetaan se konsolille

def piato(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1408&language=fi')
    update.message.reply_text(viesti)

def maija(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1402&language=fi')
    update.message.reply_text(viesti)

def lozzi(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1401&language=fi')
    update.message.reply_text(viesti)

def belvedere(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1404&language=fi')
    update.message.reply_text(viesti)

def syke(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1405&language=fi')
    update.message.reply_text(viesti)

def tilia(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1413&language=fi')
    update.message.reply_text(viesti)

def uno(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1414&language=fi')
    update.message.reply_text(viesti)

def ylisto(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1403&language=fi')
    update.message.reply_text(viesti)

def kvarkki(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=140301&language=fi')
    update.message.reply_text(viesti)

def rentukka(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1416&language=fi')
    update.message.reply_text(viesti)

def novelli(update, context):
    viesti = getRuokalistaSemma('https://www.semma.fi/modules/json/json/Index?costNumber=1409&language=fi')
    update.message.reply_text(viesti)

def getRuokalistaSemma(url):
    """Hakee ruokalistan Semman sivuilta
       return: Muotoiltu päivänruokalista"""
    # Hakee ja käsittelee json tiedoston
    htmlContent = requests.get(url, verify=True)
    jsonL = json.loads(htmlContent.text)
    # Hakee halutun päivän
    today = datetime.now().isoformat().split('T')
    print(today)
    
    # Purkaa json-tiedostosta ruokalistan haluttuun muotoon
    viesti_tele = ""

    viesti_tele += jsonL["RestaurantName"] + "\n"

    viikonruokalista = jsonL["MenusForDays"]
    for x in viikonruokalista:
        vrl_pvm = x["Date"]
        today_ruokalista = vrl_pvm.split('T')
        if today_ruokalista[0] == today[0]:
            menu = viikonruokalista[0]["SetMenus"]
            for ruokalaji in menu:
                comp = ruokalaji["Components"]
                for txt in comp:
                    viesti_tele += txt + "\n"
                viesti_tele += "\n"

    return viesti_tele


def start(update, context):
    logger.info("User {} started bot".format(update.effective_user['id']))
    update.message.reply_text("Hei ja tervetuloa käyttään ruokalista bottia!\nBotti toimii vain Semman ravintoloihin.\nSaat haluamasi ravintolan ruokalistan kutsumalla esim /piato")

def help(update, context):
    """Botin helpperi"""
    update.message.reply_text('Help!')

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(token, use_context=True) #os.getenv("TOKEN")
    
    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.dispatcher.add_handler(CommandHandler("piato", piato))
    updater.dispatcher.add_handler(CommandHandler("maija", maija))
    updater.dispatcher.add_handler(CommandHandler("lozzi", lozzi))
    updater.dispatcher.add_handler(CommandHandler("belvedere", belvedere))
    updater.dispatcher.add_handler(CommandHandler("syke", syke))
    updater.dispatcher.add_handler(CommandHandler("tilia", tilia))
    updater.dispatcher.add_handler(CommandHandler("uno", uno))
    updater.dispatcher.add_handler(CommandHandler("ylistö", ylisto))
    updater.dispatcher.add_handler(CommandHandler("kvarkki", kvarkki))
    updater.dispatcher.add_handler(CommandHandler("rentukka", rentukka))
    updater.dispatcher.add_handler(CommandHandler("novelli", novelli))

    run(updater)