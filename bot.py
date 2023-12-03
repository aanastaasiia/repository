import telebot
import sqlite3
from telebot import types
token = '6433199317:AAGXR1rrCl_2TDUAVjSiOT_enks_p9_LIr8'
bot = telebot.TeleBot(token)
conn = sqlite3.connect('database2.db', check_same_thread=False)
cursor = conn.cursor()

#создаем таблицу
cursor.execute("""CREATE TABLE IF NOT EXISTS usersuunit( 
   user_id TEXT,
   name TEXT,
   sname TEXT,
   faculty TEXT,
   groups TEXT,
   bio TEXT
   link TEXT
   interests TEXT);
""")

#функция которая будет принимать значения и заносить их в таблицу
def db_table_val(user_id: int, name: str, sname: str, faculty: str, groups: str, bio: str, link: str, interests: str):
    cursor.execute('INSERT INTO usersuunit (user_id, name, sname, faculty, groups, bio, link, interests) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, name, sname, faculty, groups, bio, link, interests))
    conn.commit()

@bot.message_handler(content_types=['text', 'photo'])

#начало работы бота, создание профиля, получение данных от пользователя
def get_text_messages(msg):
    if msg.text == '/start':
        bot.send_message(msg.chat.id, text='Привет, этот бот поможет тебе найти друзей в своем вузе. Давай заполним профиль. Как тебя зовут?')
        global iid
        iid = msg.from_user.id
        bot.register_next_step_handler(msg, fname)

    #здесь же кнопка редактировать профиль и последующие кнопки, продолжение в функции edit
    if msg.text == 'Редактировать профиль':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Изменить имя")
        btn2 = types.KeyboardButton("Изменить фамилию")
        btn3 = types.KeyboardButton("Изменить факультет")
        btn4 = types.KeyboardButton("Изменить группу")
        btn5 = types.KeyboardButton("Изменить информацию о себе")
        btn6 = types.KeyboardButton("Назад")
        markup1.add(btn1, btn2, btn3, btn4, btn5, btn6)
        change = bot.send_message(msg.chat.id, text='Здесь вы можете отредактировать профиль', reply_markup=markup1)
        bot.register_next_step_handler(change, edit)
    #здесь же кнопка поиска и последующие, продолжение в функции find
    if msg.text == 'Найти новых знакомых':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnn1 = types.KeyboardButton("Cлучайные анкеты")
        btnn2 = types.KeyboardButton("Фильтры")
        btnn3 = types.KeyboardButton("Назад")
        markup2.add(btnn1, btnn2, btnn3)
        bot.send_message(msg.chat.id, text='Вы можете посмотреть случайные анкеты или найти человека по группе или факультету в фильтре', reply_markup=markup2)
    if msg.text == 'Cлучайные анкеты':
        a = cursor.execute('SELECT * FROM usersuunit ORDER BY RANDOM() LIMIT 1')
        rand = a.fetchone()
        bot.send_message(msg.chat.id, text='Имя: '+str(rand[1])+', фамилия: '+str(rand[2])+', факультет: '+str(rand[3])+', группа: '+str(rand[4])+', о себе: '+str(rand[5])+', ссылка на профиль: '+str(rand[-1]))
    if msg.text == 'Фильтры':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnnn1 = types.KeyboardButton("По факультету")
        btnnn2 = types.KeyboardButton("По группе")
        btnnn3 = types.KeyboardButton("По интересам")
        btnnn4 = types.KeyboardButton("Назад")
        markup2.add(btnnn1, btnnn2, btnnn3, btnnn4)
        a = bot.send_message(msg.chat.id, text='Можешь найти знакомых по определенному факультету, группе или интересам', reply_markup=markup2)
        bot.register_next_step_handler(a, filtr)
    if msg.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать профиль")
        btn2 = types.KeyboardButton("Найти новых знакомых")
        btn3 = types.KeyboardButton("Посмотреть профиль")
        markup.add(btn1, btn2, btn3)
        bot.send_message(msg.chat.id, text = 'Возвращаемся на главное меню', reply_markup=markup)
    if msg.text == 'Посмотреть профиль':
        iid = msg.from_user.id
        a = cursor.execute('SELECT * FROM usersuunit WHERE user_id=?', (iid,))
        rand = a.fetchone()
        bot.send_message(msg.chat.id,
                         text='Имя: ' + str(rand[1]) + ', фамилия: ' + str(rand[2]) + ', факультет: ' + str(
                             rand[3]) + ', группа: ' + str(rand[4]) + ', о себе: ' + str(
                             rand[5]) + ', ссылка на профиль: ' + str(rand[-1]))





def filtr(msg):
    if msg.text == "По факультету":
        bot.send_message(msg.chat.id, text='Какой факультет вас интересует?')
        bot.register_next_step_handler(msg, findfaculty)


    if msg.text == "По группе":
        bot.send_message(msg.chat.id, text='Какая группа вас интересует??')
        bot.register_next_step_handler(msg, findgroup)

    if msg.text == 'По интересам':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Программирование")
        btn2 = types.KeyboardButton("Спорт")
        btn3 = types.KeyboardButton("Рисование")
        btn4 = types.KeyboardButton("Музыка")
        btn5 = types.KeyboardButton("Игры")
        btn6 = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, btn4, btn6)
        bot.register_next_step_handler(msg, findinterest)
        bot.send_message(msg.chat.id, text='Какое увлечение вас интересует?', reply_markup=markup)



    if msg.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать профиль")
        btn2 = types.KeyboardButton("Найти новых знакомых")
        btn3 = types.KeyboardButton("Посмотреть профиль")
        markup.add(btn1, btn2, btn3)
        bot.send_message(msg.chat.id, text='Возвращаемся на главное меню', reply_markup=markup)


def findfaculty(msg):
    ifaculty = str(msg.text).upper()
    a = cursor.execute('SELECT * FROM usersuunit WHERE faculty=?', (ifaculty,))
    rand = a.fetchone()
    bot.send_message(msg.chat.id, text='Имя: '+str(rand[1])+', фамилия: '+str(rand[2])+', факультет: '+str(rand[3])+', группа: '+str(rand[4])+', о себе: '+str(rand[5])+', ссылка на профиль: '+str(rand[-1]))
    bot.register_next_step_handler(msg, filtr)
def findgroup(msg):
    igroup = str(msg.text).upper()
    a = cursor.execute('SELECT * FROM usersuunit WHERE groups=?', (igroup,))
    rand = a.fetchone()
    bot.send_message(msg.chat.id, text='Имя: ' + str(rand[1]) + ', фамилия: ' + str(rand[2]) + ', факультет: ' + str(rand[3]) + ', группа: ' + str(rand[4]) + ', о себе: ' + str(rand[5]) + ', ссылка на профиль: ' + str(rand[-1]))
    bot.register_next_step_handler(msg, filtr)

def findinterest(msg):
    iinterest = str(msg.text)
    bot.register_next_step_handler(msg, filtr)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать профиль")
    btn2 = types.KeyboardButton("Найти новых знакомых")
    btn3 = types.KeyboardButton("Посмотреть профиль")
    markup.add(btn1, btn2, btn3)
    a = cursor.execute('SELECT * FROM usersuunit WHERE interests=?', (iinterest,))
    rand = a.fetchone()
    bot.send_message(msg.chat.id, text='Имя: ' + str(rand[1]) + ', фамилия: ' + str(rand[2]) + ', факультет: ' + str(rand[3]) + ', группа: ' + str(rand[4]) + ', о себе: ' + str(rand[5]) + ', ссылка на профиль: ' + str(rand[-1]), reply_markup=markup)


#миллион функций посвященным созданию профиля
def fname(msg):
    global name1
    name1 = msg.text
    bot.send_message(msg.chat.id, text='Теперь фамилия')
    bot.register_next_step_handler(msg, fsname)


def fsname(msg):
    global sname1
    sname1 = msg.text
    bot.send_message(msg.chat.id, text='Факультет')
    bot.register_next_step_handler(msg, ffaculty)

def ffaculty(msg):
    global faculty1
    faculty1 = str(msg.text).upper()
    bot.send_message(msg.chat.id, text='Группа')
    bot.register_next_step_handler(msg, fgroup)


def fgroup(msg):
    global group1
    group1 = str(msg.text).upper()
    bot.send_message(msg.chat.id, text='Расскажи о себе')
    bot.register_next_step_handler(msg, fbio)

def fbio(msg):
    global bio1
    bio1 = msg.text
    bot.send_message(msg.chat.id, text='А теперь укажи свой ник, стобы другие пользователи могли с тобой связаться. Пример: @anastasia_bagrova_1')
    bot.register_next_step_handler(msg, flink)


def flink(msg):
    global link1
    link1 = msg.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Программирование")
    btn2 = types.KeyboardButton("Спорт")
    btn3 = types.KeyboardButton("Рисование")
    btn4 = types.KeyboardButton("Музыка")
    btn5 = types.KeyboardButton("Genshin Impact")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    msg = bot.send_message(msg.chat.id, text='Для того, чтобы люди с похожими интересами могли найти тебя, укажи свое главное увлечение. Ты можешь выбрать его из уже существующих, или добавить новое', reply_markup=markup)
    bot.register_next_step_handler(msg, fend)



def fend(msg):
    interests1 = msg.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать профиль")
    btn2 = types.KeyboardButton("Найти новых знакомых")
    btn3 = types.KeyboardButton("Посмотреть профиль")
    markup.add(btn1, btn2, btn3)
    #сохранение всех данных пользователя
    db_table_val(user_id=iid, name=name1, sname=sname1, faculty=faculty1, groups=group1, bio=bio1, link=link1, interests=interests1)

    bot.send_message(msg.chat.id, text='Отлично, теперь ты можешь искать новых знакомых', reply_markup=markup)


#миллион функций посвященных редакции профиля
def edit(msg):
    if msg.text=='Назад':
        if msg.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Редактировать профиль")
            btn2 = types.KeyboardButton("Найти новых знакомых")
            btn3 = types.KeyboardButton("Посмотреть профиль")
            markup.add(btn1, btn2, btn3)
            bot.send_message(msg.chat.id, text='Возвращаемся на главное меню', reply_markup=markup)
    if msg.text == "Изменить имя":
        bot.send_message(msg.chat.id, text='Выберите новое имя')
        bot.register_next_step_handler(msg, nname)

    if msg.text == "Изменить фамилию":
        bot.send_message(msg.chat.id, text='Выберите новую фамилию')
        bot.register_next_step_handler(msg, nsname)

    if msg.text == "Изменить факультет":
        bot.send_message(msg.chat.id, text='Выберите новый факультет')
        bot.register_next_step_handler(msg, nfaculty)

    if msg.text == "Изменить группу":
        bot.send_message(msg.chat.id, text='Выберите новую группу')
        bot.register_next_step_handler(msg, ngroup)

    if msg.text == "Изменить информацию о себе":
        bot.send_message(msg.chat.id, text='Выберите новую информацию о себе')
        bot.register_next_step_handler(msg, nbio)

    if msg.text == 'Изменить ник':
        bot.send_message(msg.chat.id, text='Выберите новый ник')
        bot.register_next_step_handler(msg, nlink)

#все еще редакция.....
def nname(msg):
    bot.send_message(msg.chat.id, text='Ваше имя изменено')
    newname = msg.text
    cursor.execute("UPDATE usersuunit SET name = ? WHERE user_id = ?", (newname, iid))
    conn.commit()


def nsname(msg):
    bot.send_message(msg.chat.id, text='Ваша фамилия изменена')
    newsname = msg.text
    cursor.execute("UPDATE usersuunit SET sname = ? WHERE user_id = ?", (newsname, iid))
    conn.commit()


def nfaculty(msg):
    bot.send_message(msg.chat.id, text='Ваш факультет изменен')
    newfaculty = msg.text
    cursor.execute("UPDATE usersuunit SET faculty = ? WHERE user_id = ?", (newfaculty, iid))
    conn.commit()

def ngroup(msg):
    bot.send_message(msg.chat.id, text='Ваша группа изменена')
    newgroup = msg.text
    cursor.execute("UPDATE usersuunit SET groups = ? WHERE user_id = ?", (newgroup, iid))
    conn.commit()

def nbio(msg):
    bot.send_message(msg.chat.id, text='Ваша информация о себе изменена')
    newbio = msg.text
    cursor.execute("UPDATE usersuunit SET bio = ? WHERE user_id = ?", (newbio, iid))
    conn.commit()


def nlink(msg):
    bot.send_message(msg.chat.id, text='Ваше увлечение изменено')
    newlink = msg.text
    cursor.execute("UPDATE usersuunit SET link = ? WHERE user_id = ?", (newlink, iid))
    conn.commit()



bot.polling(none_stop=True, interval=0)
