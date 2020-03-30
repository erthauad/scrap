import requests
import mysql.connector
import sys
import datetime
import pytz
import os, ssl
from bs4 import BeautifulSoup
from plyer import notification
import time
import telegram
from telegram.ext import Updater

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="corona"
	)

kursor = mydb.cursor()

kursor.execute("delete from corona")

# r = requests.get("https://pomber.github.io/covid19/timeseries.json").json()

# number = 1

# for y in r['Indonesia']:

# 	kursor.execute("insert into corona(id,negara,date,confirmed,deaths,recovered,datetime) values(%s,%s,%s,%s,%s,%s,%s)", (number,'Indonesia',y['date'],y['confirmed'],y['deaths'],y['recovered'],datetime.datetime.now(pytz.timezone('Asia/Jakarta'))))

# 	number += 1

page = requests.get('https://www.worldometers.info/coronavirus/country/indonesia/').text
soup = BeautifulSoup(page, 'html.parser')
soup.encode('utf-8')

# cases = soup.find("div", {"class": "maincounter-number"}).find("span", {"style", {"color" : "#aaa"}})[0].get_text().strip()

cases = soup.find_all("div", {"class": "maincounter-number"})

hasil = []

for x in cases:

	children = x.findChildren("span", recursive=True)

	for y in children:
		
		iwant = y.text.split(' ')[0].strip()

		hasil.append(iwant)


tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

dt_string = tanggal.strftime("%Y-%m-%d")

kursor.execute("insert into corona(id,negara,date,confirmed,deaths,recovered,datetime) values(%s,%s,%s,%s,%s,%s,%s)", ('1','Indonesia',dt_string,hasil[0].replace(",",""),hasil[1].replace(",",""),hasil[2].replace(",",""),datetime.datetime.now(pytz.timezone('Asia/Jakarta'))))

mydb.commit()

bot = telegram.Bot(token='1047606248:AAGEigVEKaziXVbeBqS8AYy8KuQ90LUP--c')

updater = Updater(token='1047606248:AAGEigVEKaziXVbeBqS8AYy8KuQ90LUP--c', use_context=True)

dispatcher = updater.dispatcher

bot.send_message(chat_id='-326597063', text="Kasus COVID-19 Tanggal " + str(dt_string) + "\nTerinfeksi : " + hasil[0] + "\nMeninggal : " + hasil[1] + "\nSembuh : " + hasil[2] + "")

# while True:
# 	bot.send_message(chat_id='-326597063', text="Kasus COVID-19 Tanggal " + str(datetime.date.today()) + "\nTerinfeksi : " + hasil[0] + "\nMeninggal : " + hasil[1] + "\nSembuh : " + hasil[2] + "")
# 	time.sleep(10)


# print(bot)

# print('--------------------------------------')
# print(number, "data berhasil di tambahkan")

