# -*- coding: cp1251 -*-

from libraries import *

token = '5120895038:AAF4qt2-_-F2h4CdsyeJCZnm40my0u7pRzQ'
bot = telebot.TeleBot(token)
list_user = []
r = sr.Recognizer()
language = 'en_EN'


class User:

    def __init__(self, id=0, endMessage=False, recoms="", flag=True):
        self.__text = ''
        self.__id = id
        self.__endMessage = endMessage
        self.recoms = recoms
        self.flag = flag

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

    def set_recom(self, recom):
        self.recoms = recom

    def set_flag(self):
        self.flag = not self.flag


if __name__ == '__main__':

    @bot.message_handler(commands=['start'])
    def start(message):
        id_u = message.chat.id
        list_user.append(User(id_u))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_start = types.KeyboardButton("Start note")
        markup.add(button_start)
        bot.send_message(message.chat.id, text='HI', reply_markup=markup)


    @bot.message_handler(content_types=['voice'])
    def get_audio_messages(message):
        id_u = message.chat.id
        try:
            file_info = bot.get_file(message.voice.file_id)
            path = os.path.splitext(file_info.file_path)[0]
            fname = os.path.basename(path)
            doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

            result = voice_text.query(doc.content)
            data = result['text']

            prediction = model.predict(data)

            bot.send_message(id_u, text=prediction[1])
        except sr.UnknownValueError as e:
            bot.send_message(message.from_user.id, "Прошу прощения, но я не разобрал сообщение, или оно поустое...")

        except Exception as e:
            bot.send_message(message.from_user.id,
                             "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")


    @bot.message_handler(content_types=['text'])
    def func(message):

        id_u = message.chat.id
        user = User()
        recommendations = ""

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
                recom = types.KeyboardButton("Show recommendation")
                start_button = types.KeyboardButton("Start note")

                markup.add()
                bot.send_message(id_u, text="I try to analyze...", reply_markup=markup)

                prediction = model.predict(user.get_text())
                user.set_recom(prediction[1])

                markup.add(recom, start_button)
                bot.send_message(id_u, text="I found out that now you feel " + prediction[0], reply_markup=markup)
                user.delete_text()
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(id_u, text="Oops! Your notes are empty. Please, tell me, what events"
                                            " were happened with you today?", reply_markup=markup)

        elif message.text == 'Show recommendation':
            try:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                start_button = types.KeyboardButton("Start note")
                markup.add(start_button)

                bot.send_message(id_u, text=user.recoms, reply_markup=markup)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(id_u, text="Oops! Your notes are empty. Please, tell me, what events"
                                            " were happened with you today?", reply_markup=markup)

        elif user.get_endMessage():
            user.append_message(str(message.text))


    bot.polling(none_stop=True, interval=0)
