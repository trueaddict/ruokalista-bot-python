import logging
import time
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import json
import requests

#logging
logging.basicConfig(format='%(astime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger()


#mode switch
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
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

    pvm_lista = today[0].split('-')
    today_tulostu = pvm_lista[2] + "." + pvm_lista[1] + "." + pvm_lista[0]

    viesti_tele += jsonL["RestaurantName"] +" - " + today_tulostu +  "\n\n"

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

def ilokivi(update, context):
    ilokivi_url = 'https://www.ilokivi.fi/ravintola/lounas'
    htmlContent = requests.get(ilokivi_url, verify=True).text
    html = BeautifulSoup(htmlContent, 'html.parser')

    lunch_div = html.find('div', attrs={'class':'content'})
    lunch = lunch_div.find('p')


    for text in lunch.find_all('i'):
        text.unwrap()
    
    for text in lunch.find_all('br'):
        text.replace_with('\n\n')

    pvm_lista = datetime.now().isoformat().split('T')[0].split('-')
    today_tulostu = pvm_lista[2] + "." + pvm_lista[1] + "." + pvm_lista[0]
    
    update.message.reply_text("Ravintola Ilokivi - " + today_tulostu + "\n" + lunch.text)
    

def start(update, context):
    logger.info("User {} started bot".format(update.effective_user['id']))
    update.message.reply_text("Hei ja tervetuloa käyttämään ruokalistabottia!\nBotti toimii Semman ravintoloihin sekä Ilokiven ravintolaan.\nSaat haluamasi ravintolan ruokalistan kutsumalla esim /piato\nKaikki mahdolliset komennot saat komennolla /help")

def help(update, context):
    """Botin helpperi / komennot"""
    update.message.reply_text('Botin komennot:\n/start\n/help\n/piato\n/maija\n/lozzi\n/belvedere\n/syke\n/tilia\n/uno\n/ylisto\n/kvarkki\n/rentukka\n/novelli\n/ilokivi')

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(os.getenv("TOKEN"), use_context=True) 
    
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))

    updater.dispatcher.add_handler(CommandHandler("piato", piato))
    updater.dispatcher.add_handler(CommandHandler("maija", maija))
    updater.dispatcher.add_handler(CommandHandler("lozzi", lozzi))
    updater.dispatcher.add_handler(CommandHandler("belvedere", belvedere))
    updater.dispatcher.add_handler(CommandHandler("syke", syke))
    updater.dispatcher.add_handler(CommandHandler("tilia", tilia))
    updater.dispatcher.add_handler(CommandHandler("uno", uno))
    updater.dispatcher.add_handler(CommandHandler("ylisto", ylisto))
    updater.dispatcher.add_handler(CommandHandler("kvarkki", kvarkki))
    updater.dispatcher.add_handler(CommandHandler("rentukka", rentukka))
    updater.dispatcher.add_handler(CommandHandler("novelli", novelli))

    updater.dispatcher.add_handler(CommandHandler("ilokivi", ilokivi))

    run(updater)