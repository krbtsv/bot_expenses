from datetime import date
import telebot
import gspread
from hidden import bot_token
from hidden import google_sheets_id

bot = telebot.TeleBot(bot_token)
sa = gspread.service_account(filename='service_account.json')

# приветствуем пользователя и говорим что умеем
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, я буду фиксировать ваши расходы в таблицу. Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:')

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    try:
        today = date.today().strftime('%d.%m.%Y')

        #  разделяем сообщение на 2 части, категория и цена
        category, price = message.text.split('-', 1)
        text_message = f'На {today} в таблицу расходов добавлена запись: категория {category}, сумма {price} руб.'
        bot.send_message(message.chat.id, text_message)

        # открываем Google таблицу и добавляем запись
        sh = sa.open_by_key(google_sheets_id)
        sh.sheet1.append_row([today, category, price])
    except:
        # если пользователь ввел неправильную информацию, оповещаем его и просим вводить повторно
        bot.send_message(message.chat.id, 'Ошибка! Неправильный формат данных!')

    bot.send_message(message.chat.id, 'Введите расход через дефис в виде [КАТЕГОРИЯ-ЦЕНА]:')

if __name__ == '__main__':
    bot.polling(none_stop=True)