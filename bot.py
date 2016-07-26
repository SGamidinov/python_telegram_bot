import sqlite3
import time
import random
import json
import requests


try:
    import telepot
except(ImportError, IOError):
    print('not found a telegram api - require telepot' + '\n'
          'run command: "pip install telepot"')
    exit('Closing...')


token = input('Введите ваш токен ключ: ')

"""создание шаблона базы данных"""
DataBaseName = 'userd.db'
conn = sqlite3.connect(DataBaseName)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS cities (names)")
c.execute("CREATE TABLE IF NOT EXISTS users (id, msg)")
j = requests.get('http://api.hh.ru/areas')
foo = json.loads(j.content.decode('utf-8'))

"""проводит проверку на заполненность поля names в таблице
   cities и если нет заполняет их именами городов"""
c.execute('SELECT * FROM cities')
if len(c.fetchall()) == 0:
    for i in foo:
        f = i['areas']
        for j in f:
            d = j['areas']
            for e in d:
                g = [(e['name'])]
                c.execute("INSERT INTO cities VALUES (?)", g)
    conn.commit()
else:
    print('-' * 70)


def handle(msg):
    text_type, chat_type, chat_id = telepot.glance(msg)
    answer_names = []
    g = msg
    ask = g['text']

    """открытие бд для чтение внутри функции"""
    DataBaseName = 'userd.db'
    conn = sqlite3.connect(DataBaseName)
    c = conn.cursor()
    c.execute('SELECT * FROM cities')

    """получение все имен для отбора из них по первой букве"""
    all_names = c.fetchall()
    if ask != '/start':
        bot.sendChatAction(chat_id, 'typing')
        answer_names.clear()
        c.execute("INSERT INTO users VALUES (?,?)", (chat_id, ask))
        conn.commit()
        for row in all_names:
            h = row[0]
            if h[0].title() == ask[-1].title():
                answer_names.append(row[0])
        g = len(answer_names)
        if g == 0:
            bot.sendMessage(chat_id, 'Воав, потише братишка. Я не '
                            'знаю городов на такую букву. '
                            'Давай на другую букву.')
        else:
            choice = random.randrange(0, g)
            time.sleep(1)
            bot.sendMessage(chat_id, answer_names[choice])


bot = telepot.Bot(token)
bot.message_loop(handle)
print('Listening ...')
while True:
    f = input('input yes for closing ==> ')
    print('-' * 72)
    if f == 'yes':
        conn.close()
        break
