import telebot
import time
import random

bot = telebot.TeleBot('TOKEN')  # здесь указываем токен, который нам выдал FatherBot
list_id = ['CHAT_ID']  # здесь указываем chat_id пользователей, которые будут пользоваться ботом
string_words = ''
s = set()


def pull_words():
    global string_words
    list_words = []  # извлекаем все слова с этот список
    with open('list_words.txt', encoding='utf8') as lw:
        for i in lw:
            list_words.append(i.replace('\n', ''))
    temporary_list = []  # создаем временный список для хранения 30 слов
    while len(temporary_list) != 30:
        temporary_list = random.sample(list_words, 30)  # добавляем в него случайные слова
        temporary_list = list(set(temporary_list))  # используем множества для уникальности слов
    temporary_list = sorted(temporary_list)  # сортируем список по алфавиту
    string_words = '        '.join(temporary_list)  # создаем строку
    return string_words


def delete():
    global string_words, s
    string_words = ''
    s.clear()


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.id in list_id:
        bot.send_message(message.from_user.id, text=f'Привет, я помогу тебе прокачать оперативную память!\n'
                                                    f'Жми на 👇\n\n'
                                                    f'             /play')


@bot.message_handler(commands=['play'])
def starting_message(message):
    if message.from_user.id in list_id:
        delete()
        bot.send_message(message.from_user.id, text=f'Через 5 сек появится список из 30 слов '
                                                    f'и исчезнет через 2 минуты.\n\n'
                                                    f'После того, как исчезнет сообщение, '
                                                    f'слова из списка вводи по одному!\n\n'
                                                    f'Постарайся запомнить все слова.\n'
                                                    f'Желаю удачи!')
        start_1 = time.time()
        while int(time.time() - start_1) != 5:
            pass
        pull_words()
        del_msg = bot.send_message(message.from_user.id, text=f'{string_words}')
        start_2 = time.time()
        while int(time.time() - start_2) != 120:
            pass
        bot.delete_message(message.from_user.id, del_msg.id)
        bot.send_message(message.from_user.id, text=f'Вводи слово: ')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.from_user.id in list_id:
        global string_words, s
        new_list = string_words.split()
        m = str(message.text).lower().replace(' ', '').replace('ё', 'е')
        if m in new_list:
            s.add(m)
            bot.send_message(message.from_user.id, text=f'Верно указанных слов: {len(s)}')
        else:
            bot.send_message(message.from_user.id, text=f'Неверно!')
        if len(s) == 30:
            bot.send_message(message.from_user.id, text=f'Поздравляю, у тебя отличная память!\n'
                                                        f'Хочешь ещё раз?\n'
                                                        f'Жми на 👇\n\n'
                                                        f'             /play')
            s.clear()


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as E:
        time.sleep(1)
