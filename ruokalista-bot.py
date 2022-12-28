import logging
import time
import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

import json
import requests

#logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
        PORT = int(os.environ.get("PORT", "443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TOKEN,
                                webhook_url="https://python-ruokalista-bot.herokuapp.com/"+TOKEN)
        updater.idle()
else:
    logger.error("No MODE specified!")
    sys.exit(1)


base_url_semma = 'https://www.semma.fi/modules/json/json/Index'
base_url_compass = 'https://www.compass-group.fi/menuapi/feed/json'
def createUrl(costNumber, base_url):
    return base_url + '?costNumber={0}&language=fi'.format(costNumber)

# Haetaan webistä ruokalista ja tulostetaan se konsolille

# Jyväskylä

def piato(update, context):
    # 1408
    getRuokalista(update, createUrl(1408, base_url_semma))

def maija(update, context):
    getRuokalista(update, createUrl(1402, base_url_semma))

def lozzi(update, context):
    getRuokalista(update, createUrl(1401, base_url_semma))

def belvedere(update, context):
    getRuokalista(update, createUrl(1404, base_url_semma))

def syke(update, context):
    getRuokalista(update, createUrl(1405, base_url_semma))

def tilia(update, context):
    getRuokalista(update, createUrl(1413, base_url_semma))

def uno(update, context):
    getRuokalista(update, createUrl(1414, base_url_semma))

def ylisto(update, context):
    getRuokalista(update, createUrl(1403, base_url_semma))

def kvarkki(update, context):
    # 140301
    getRuokalista(update, createUrl(140301, base_url_semma))

def rentukka(update, context):
    # 1416
    getRuokalista(update, createUrl(1416, base_url_semma))

def novelli(update, context):
    # 1409
    getRuokalista(update, createUrl(1409, base_url_semma))

def fiilu(update, context):
    # 3364
    getRuokalista(update, createUrl(3364, base_url_compass))

def taide(update, context):
    # 0301
    getRuokalista(update, createUrl('0301', base_url_compass))

# Kuopio

def tietoteknia(update, context):
    # 0439
    getRuokalista(update, createUrl('0439', base_url_compass))

def snellmania(update, context):
    # 0437
    getRuokalista(update, createUrl('0437', base_url_compass))

def canthia(update, context):
    # 0436
    getRuokalista(update, createUrl('0436', base_url_compass))

def mediteknia(update, context):
    # 0442
    getRuokalista(update, createUrl('0442', base_url_compass))
    
        
# Vantaa
def aviapolis(update, context):
    # 3103
    getRuokalista(update, createUrl(3103, base_url_compass))


def getRuokalista(update, url):
    """Hakee ruokalistan Compass Groupin sivuilta
       return: Muotoiltu päivänruokalista"""
    logger.info("User {0} fetched menu for {1}".format(update.effective_user['id'], url))
    # Hakee ja käsittelee json tiedoston
    htmlContent = requests.get(url, verify=True)
    jsonL = json.loads(htmlContent.text)
    if jsonL["RestaurantName"] == None:
        update.message.reply_text(jsonL['ErrorText'])
        return
    
    # Hakee halutun päivän
    today = datetime.now().isoformat().split('T')
    print(today)
    
    # Purkaa json-tiedostosta ruokalistan haluttuun muotoon
    viesti = ""

    pvm_lista = today[0].split('-')
    today_tulostu = pvm_lista[2] + "." + pvm_lista[1] + "." + pvm_lista[0]

    viesti += jsonL["RestaurantName"] +" - " + today_tulostu + ' - <a href="' + jsonL['RestaurantUrl'] +  '">Lisätiedot</a> \n\n'

    viikonruokalista = jsonL["MenusForDays"]
    for x in viikonruokalista:
        vrl_pvm = x["Date"]
        today_ruokalista = vrl_pvm.split('T')
        if today_ruokalista[0] == today[0]:
            menu = viikonruokalista[0]["SetMenus"]
            for ruokalaji in menu:
                comp = ruokalaji["Components"]
                for txt in comp:
                    viesti += txt + "\n"
                viesti += "\n"

    update.message.reply_text(viesti, parse_mode=ParseMode.HTML)

def ilokivi(update, context):
    logger.info("User {} fetched menu for Ilokivi".format(update.effective_user['id']))
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


def debug(update, context):
    update.message.reply_text('[LINK](https://google.fi)', parse_mode=ParseMode.MARKDOWN_V2)


def start(update, context):
    logger.info("User {} started bot".format(update.effective_user['id']))
    update.message.reply_text(
"""
Hei ja tervetuloa käyttämään ruokalistabottia!
Botti toimii Jyväskylässä Semman ja Ilokiven ravintoloihin sekä muutamaan Itä-Suomen yliopiston ravintolaan.
Saat haluamasi ravintolan ruokalistan kutsumalla esim /piato
Kaikki mahdolliset komennot saat komennolla /help
""")

def help(update, context):
    """Botin helpperi / komennot"""
    update.message.reply_text(
"""
Botin komennot:
/start
/help

Jyväskylä:
/piato
/maija
/lozzi
/belvedere
/syke
/tilia
/uno
/ylisto
/kvarkki
/rentukka
/novelli
/taide
/ilokivi

Kuopio:
/tietoteknia
/snellmania
/canthia
/mediteknia

Vantaa:
/aviapolis
""")

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(os.getenv("TOKEN"), use_context=True) 
    
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("debug", debug))

    # Jyväskylä
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
    updater.dispatcher.add_handler(CommandHandler("fiilu", fiilu))
    updater.dispatcher.add_handler(CommandHandler("taide", taide))

    updater.dispatcher.add_handler(CommandHandler("ilokivi", ilokivi))

    # Kuopio
    updater.dispatcher.add_handler(CommandHandler("tietoteknia", tietoteknia))
    updater.dispatcher.add_handler(CommandHandler("snellmania", snellmania))
    updater.dispatcher.add_handler(CommandHandler("canthia", canthia))
    updater.dispatcher.add_handler(CommandHandler("mediteknia", mediteknia))

    # Vantaa
    updater.dispatcher.add_handler(CommandHandler("aviapolis", aviapolis))

    run(updater)