import telebot
from telebot import types
from SQL import SqlStudents, ReportsId
import random


bot_token = "5484159093:AAEbNDrJxZZuayFeVg9g32PhxQ2pIyZ0fHk"
bot = telebot.TeleBot(bot_token)
sql_student = SqlStudents()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    call_btn = types.InlineKeyboardButton(text='Войти в аккаунт', callback_data='Войти в аккаунт')
    markup.add(call_btn)
    text = 'Привет! Я - 🤖 бот KeGO!'
    text += ' Моя задача - держать в фокусе твои цели и помочь тебе достигнуть их в процессе обучения.'
    bot.send_message(message.chat.id, text=text)
    check = sql_student.check_up(message.chat.id)
    global ch_id
    ch_id = message.chat.id
    if check is None:
        text = 'Также я постараюсь сделать всё возможное, чтобы ты не потерял мотивацию.'
        bot.send_message(message.chat.id, text=text)
        bot.send_message(message.chat.id, text='Для начала давай познакомимся! Отправь мне свое полное имя:')
        bot.register_next_step_handler(message, get_name)
    else:
        global user_name
        user_name = check
        text = 'Также я постараюсь сделать всё возможное, чтобы ты не потерял мотивацию.'
        bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text='Я не виноват')


@bot.message_handler(content_types=['text'])
def get_name(message):
    global user_name
    user_name = message.text
    bot.send_message(message.chat.id, text='📧 Отправь свою электронную почту:'.format(message.from_user))
    bot.register_next_step_handler(message, get_email)


def get_email(message):
    id_chat = message.chat.id
    email = message.text
    res_db = sql_student.log_in([id_chat, user_name, email])
    markup = types.InlineKeyboardMarkup()
    call_btn = types.InlineKeyboardButton(text='Войти в аккаунт', callback_data='Войти в аккаунт')
    markup.add(call_btn)
    bot.send_message(message.chat.id, text='Окей, я тебя запомнил.', reply_markup=markup)


def get_task(message):
    sql_report_id = ReportsId(ch_id)
    sql_student.update_data_in_table(message.text, 'my_task', message.chat.id)
    sql_report_id.task_update(message.text, '')
    text = 'Выберите рефлексию:'
    markup = types.InlineKeyboardMarkup()
    call_btn20 = types.InlineKeyboardButton(text='💼️-♻️-🗑', callback_data='Игра чемодан')
    call_btn21 = types.InlineKeyboardButton(text=' ', callback_data=' ')
    call_btn22 = types.InlineKeyboardButton(text='  ', callback_data='  ')
    call_btn23 = types.InlineKeyboardButton(text=' ', callback_data='  ')
    markup.add(call_btn20, call_btn21, call_btn22,)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


def give_report(message):
    markup = types.InlineKeyboardMarkup()
    call_btn78 = types.InlineKeyboardButton(text='Вернутся в главное меню', callback_data='GO')
    markup.add(call_btn78)
    num = message.text
    if num.isdigit():
        if int(num) > 0:
            sql_report_id = ReportsId(ch_id)
            reports = sql_report_id.get_all_reports()
            text = reports[int(num)-1][0]
            bot.send_message(message.chat.id, text=text, reply_markup=markup)


def suitcase(message):
    sql_student.update_data_in_table(message.text, 'suitcase', message.chat.id)
    text = 'Отлично! Заполни остальное'
    markup = types.InlineKeyboardMarkup()
    call_btn52 = types.InlineKeyboardButton(text='♻️', callback_data='Мясорубка')
    call_btn53 = types.InlineKeyboardButton(text='🗑', callback_data='Корзина')
    call_btn6 = types.InlineKeyboardButton(text='Выбрать другой вид рефлексии',
                                           callback_data='Выбрать другой вид рефлексии')
    call_btn7 = types.InlineKeyboardButton(text='Я закончил сортировку',
                                           callback_data='Я закончил сортировку')
    markup.add(call_btn52, call_btn53, call_btn6, call_btn7)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


def grinder(message):
    sql_student.update_data_in_table(message.text, 'grinder', message.chat.id)
    text = 'Молодец! Продолжай в том же духе'
    markup = types.InlineKeyboardMarkup()
    call_btn52 = types.InlineKeyboardButton(text='💼️', callback_data='Чемодан')
    call_btn53 = types.InlineKeyboardButton(text='🗑', callback_data='Корзина')
    call_btn6 = types.InlineKeyboardButton(text='Выбрать другой вид рефлексии',
                                           callback_data='Выбрать другой вид рефлексии')
    call_btn7 = types.InlineKeyboardButton(text='Я закончил сортировку', callback_data='Я закончил сортировку')
    markup.add(call_btn52, call_btn53, call_btn6, call_btn7)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


def basket(message):
    sql_student.update_data_in_table(message.text, 'basket', message.chat.id)
    text = 'Хорошо! У тебя отлично получается'
    markup = types.InlineKeyboardMarkup()
    call_btn52 = types.InlineKeyboardButton(text='💼️', callback_data='Чемодан')
    call_btn53 = types.InlineKeyboardButton(text='♻ ', callback_data='Мясорубка')
    call_btn7 = types.InlineKeyboardButton(text='Я закончил сортировку',
                                           callback_data='Я закончил сортировку')
    call_btn6 = types.InlineKeyboardButton(text='Выбрать другой вид рефлексии',
                                           callback_data='Выбрать другой вид рефлексии')
    markup.add(call_btn52, call_btn53, call_btn6, call_btn7)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup = types.InlineKeyboardMarkup()

    if call.data == 'Войти в аккаунт':
        call_btn = types.InlineKeyboardButton(text='GO', callback_data='GO')
        markup.add(call_btn)
        bot.send_message(call.message.chat.id, 'Вход в аккаунт выполнен успешно')
        bot.send_message(call.message.chat.id, text=f'Рад тебя видеть, {user_name}! Давай начнем!', reply_markup=markup)

    elif call.data == 'GO':
        call_btn10 = types.InlineKeyboardButton(text='Мотивация', callback_data='Мотивация')
        call_btn11 = types.InlineKeyboardButton(text='Рефлексия', callback_data='Рефлексия')
        call_btn12 = types.InlineKeyboardButton(text='Мои задачи', callback_data='Мои задачи')
        markup.add(call_btn10, call_btn11, call_btn12)
        text = 'Чем займемся?'
        bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == 'Рефлексия':
        call_btn30 = types.InlineKeyboardButton(text='Я передумал', callback_data='GO')
        markup.add(call_btn30)
        text2 = 'Что рефлексируем? (Введите выполненую задачу, которую вы хотите проанализировать)'
        bot.edit_message_text(text2, call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.register_next_step_handler(call.message, get_task)

    elif call.data == 'Игра чемодан':
        call_btn51 = types.InlineKeyboardButton(text='💼', callback_data='Чемодан')
        call_btn52 = types.InlineKeyboardButton(text='♻️', callback_data='Мясорубка')
        call_btn53 = types.InlineKeyboardButton(text='🗑', callback_data='Корзина')
        call_btn6 = types.InlineKeyboardButton(text='Выбрать другой вид рефлексии',
                                               callback_data='Выбрать другой вид рефлексии')
        markup.add(call_btn51, call_btn52, call_btn53, call_btn6)
        text1 = 'ЧЕМОДАН-КОРЗИНА-МЯСОРУБКА \nПравила: \nЧемодан💼 - напиши наиболее важный момент, '
        text1 += 'который вынес от работы'
        text1 += ' (в группе, на занятии), готов забрать с собой и использовать в своей деятельности. \nКорзина🗑'
        text1 += ' - что оказалось ненужным, бесполезным и что можно отправить в «мусорную корзину». \nМясорубка♻'
        text1 += ' - напиши то, что оказалось интересным, но пока не готовым к употреблению в своей работе. '
        text1 += 'Что нужно еще додумать, доработать, «докрутить».'
        bot.edit_message_text(text1, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'Чемодан':
        text1 = 'Напишите то, что хотите положить в чемодан'
        bot.edit_message_text(text1, call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.register_next_step_handler(call.message, suitcase)

    elif call.data == 'Мясорубка':
        text1 = 'Напишите то, что хотите положить в мясорубку'
        bot.edit_message_text(text1, call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.register_next_step_handler(call.message, grinder)

    elif call.data == 'Корзина':
        text1 = 'Напишите то, что хотите положить в корзину'
        bot.edit_message_text(text1, call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.register_next_step_handler(call.message, basket)

    elif call.data == 'Выбрать другой вид рефлексии':
        text = 'Выберите рефлексию:'
        markup = types.InlineKeyboardMarkup()
        call_btn20 = types.InlineKeyboardButton(text='💼️-♻️-🗑', callback_data='Игра чемодан')
        call_btn21 = types.InlineKeyboardButton(text=' ', callback_data=' ')
        call_btn22 = types.InlineKeyboardButton(text='  ', callback_data='  ')
        # call_btn23 = types.InlineKeyboardButton(text='  ', callback_data='  ')
        markup.add(call_btn20, call_btn21, call_btn22, )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'Я закончил сортировку':
        task = sql_student.get_data_in_table('my_task', ch_id)[0]
        suit = sql_student.get_data_in_table('suitcase', ch_id)[0]
        grind = sql_student.get_data_in_table('grinder', ch_id)[0]
        bask = sql_student.get_data_in_table('basket', ch_id)[0]
        str = f'Решая задачу {task}, я проанализировал свои результаты:\n '
        str += f'1.Самое полезное, что я узнал было {suit}\n '
        str += f'2.Мне нужно вернуться и поискать дополнительную информацию насчет {grind},так как я чувствую,'
        str += f' что это важно, но я несовсем все понял и осознал. \n 3.Я считаю, что мог бы обойтись и без'
        str += f' {bask}, не думаю, что эти знания принесут мне пользу в будущем.'
        markup = types.InlineKeyboardMarkup()
        call_btn40 = types.InlineKeyboardButton(text='Вернутся в главное меню', callback_data='GO')
        markup.add(call_btn40)
        sql_report_id = ReportsId(ch_id)
        sql_report_id.task_update(task, str)
        bot.send_message(call.message.chat.id, text=str, reply_markup=markup)

    elif call.data == 'Мои задачи':
        call_btn35 = types.InlineKeyboardButton(text='Вернутся назад', callback_data='GO')
        markup.add(call_btn35)
        sql_report_id = ReportsId(ch_id)
        tasks = sql_report_id.get_all_tasks()
        msg = ''
        for index in range(len(tasks)):
            msg += f'\n {index+1}) {tasks[index][0]}'
        text2 = 'Здесь вы можете посмотреть задачи, которые вы проанализировали вместе с KeGO!:'
        bot.send_message(call.message.chat.id, text=text2)
        text3 = msg
        bot.send_message(call.message.chat.id, text=text3)
        text4 = 'Введите номер задачи, чтобы узнать подробнее'
        bot.send_message(call.message.chat.id, text=text4, reply_markup=markup)
        bot.register_next_step_handler(call.message, give_report)

    elif call.data == 'Мотивация':
        sql_report_id = ReportsId(ch_id)
        tasks = sql_report_id.get_all_tasks()
        n = len(tasks)
        if n > 5:

            text5 = f'Ты уже сделал {n}  задач и остановишься на этом?'
        else:
            text5 = f'Ты выполнил всего лишь {n} задач, а у сына маминой подруги  {random.randint(100, 1000)}… Догоняй!'

        bot.send_message(call.message.chat.id, text=text5, reply_markup=markup)

    elif call.data == 'Кто это сказал?':
        call_btn5 = types.InlineKeyboardButton(text='Правила', callback_data='Правила Чемодана')
        call_btn6 = types.InlineKeyboardButton(text='Назад', callback_data='Меню игр')
        markup.add(call_btn5, call_btn6)
        bot.edit_message_text('Выбрана игра🧳 чемодан. Ознакомся с правилами перед тем как начать.',
                              call.message.chat.id, call.message.message_id, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
