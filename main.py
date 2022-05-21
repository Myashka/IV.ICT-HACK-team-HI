from libraries import *


class User:

    def __init__(self, id=0, endMessage=False):
        self.__text = ''
        self.__id = id
        self.__endMessage = endMessage

    def append_message(self, message):
        self.__text = self.__text + "\n" + message

    def get_id(self):
        return self.__id

    def get_text(self):
        return self.__text

    def get_endMessage(self):
        return self.__endMessage

    def changeEndMessage(self):
        self.__endMessage = not self.__endMessage

    def delete_text(self):
        self.__text = ''


if __name__ == '__main__':
    token = '5120895038:AAF4qt2-_-F2h4CdsyeJCZnm40my0u7pRzQ'
    bot = telebot.TeleBot(token)
    list_user = []


    @bot.message_handler(commands=['start'])
    def start(message):
        id_u = message.chat.id
        list_user.append(User(id_u))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton("Start note")
        markup.add(button_start)
        bot.send_message(message.chat.id, text='дякую', reply_markup=markup)


    @bot.message_handler(content_types=['text'])
    def func(message):

        id_u = message.chat.id
        user = User()

        for curr_user in list_user:
            if curr_user.get_id() == id_u:
                user = curr_user
                break

        if message.text == 'Start note':
            user.changeEndMessage()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            end_button = types.KeyboardButton("End note")
            markup.add(end_button)
            bot.send_message(id_u, text='Start writing your notes', reply_markup=markup)

        elif message.text == 'End note':
            try:
                user.changeEndMessage()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                start_button = types.KeyboardButton("Start note")
                markup.add(start_button)
                prediction = model.predict(user.get_text())
                bot.send_message(id_u, text=prediction, reply_markup=markup)
                user.delete_text()
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(id_u, text="Oops! Your notes are empty", reply_markup=markup)

        elif user.get_endMessage():
            user.append_message(str(message.text))


    bot.polling(none_stop=True, interval=0)
