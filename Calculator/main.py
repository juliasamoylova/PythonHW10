from asyncore import dispatcher
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)  
#Ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#Определение константы этапов разговора
CHOISE, RATIONAL_ONE, RATIONAL_TWO, OPERATIONS_RATIONAL, OPERATIONS_COMPLEX, COMPLEX_ONE, COMPLEX_TWO = range(7)

#функция обратного вызова точки входа в разговор

def start(update, _):
    update.message.reply_text(
        'ДОбро пожаловать в калькулятор. Введите, с какими числами хотите сделать опреацию.\n'
        'Команда \cancel, чтобы прекратить разговор.\n\n'
        )
    update.message.reply_text(
        '1 - для операций с рациональными числами: \n2 - для опреаций с комплексными числами: \n3 - для выхода \n'
    )    
    return CHOISE

def choise(update, context):
    user = update.message.from_user
    logger.info("Выбор опреации: %s: %s", user.first_name, update.message.text)
    user_choise = update.message.text
    if user_choise in '123':
        if user_choise == '1':
            update.message.reply_text(
                'Введите первое рациональное число'
            )
            return RATIONAL_ONE
        if user_choise == '2':
            context.bot.send_message(
                update.effective_chat.id, 'Введите Re и Im первого числа через ПРОБЕЛ '
            )    
            return COMPLEX_ONE
    else:
        update.message.reply_text('Это не то.\n 1 - для операций с рациональными числами: \n2 - для опреаций с комплексными числами: \n3 - для выхода \n')

def rational_one(update, context):
    user = update.message.from_user   
    logger.info("Пользователь ввел число: %s: %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_one'] = get_rational
        update.message.reply_text(
            'Введите второе рациональное'
        )
        return RATIONAL_TWO
    else:
        update.message.reply_text(
            'Нужно ввести число'
        )

def rational_two(update, context):
    user = update.message.from_user   
    logger.info("Пользователь ввел число: %s: %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_two'] = get_rational
        update.message.reply_text(
            'Выберите операцию с числами: \n\n+ - для сложения: \n - - для вычитания: \n * - для умножения: \n / - для деления: \n'
        )
        return OPERATIONS_RATIONAL


def operations_rational(update, context):
    user = update.message.from_user   
    logger.info("Пользователь выбрал операцию: %s: %s", user.first_name, update.message.text)
    rational_one = context.user_data.get('rational_one')
    rational_two = context.user_data.get('rational_two')
    user_choise = update.message.text
    if user_choise in '+-/*':
        if user_choise == '+':
            result = rational_one + rational_two
        if user_choise == '-':
            result = rational_one - rational_two
        if user_choise == '*':
            result = rational_one * rational_two
        if user_choise == '/':
            try:
                result = rational_one / rational_two
            except:
                update.message.reply_text('Деление на ноль запрещено')
        update.message.reply_text(
            f'Результат: {rational_one} + {rational_two} = {result}'
        )              
        return ConversationHandler.END
    else:
        update.message.reply_text('Это не то. Введите +-*/')

def complex_one(update, context):
    user = update.message.from_user
    logger.info("Пользователь ввел число: %s: %s", user.first_name, update.message.text)
    user_choise = update.message.text
    test = user_choise.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choise = user_choise.split(' ')
        complex_one = complex(int(user_choise[0]), int(user_choise[1]))
        context.user_data['complex_one'] = complex_one
        update.message.reply_text(
            f'Первое число {complex_one}, Введите Re и Im второго числа через ПРОБЕЛ: '
        )
    else:
        update.message.reply_text('Это не то. Введите Re и Im первого числа через ПРОБЕЛ: ') 


def complex_two(update, context):
    user = update.message.from_user
    logger.info(
        'Пользователь ввел число %s: %s', user.first_name, update.message_text
    )
    user_choice = update.message.text
    test = user_choice.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choise = user_choise.split(' ')
        complex_two = complex(int(user_choise[0]), int(user_choise[1]))
        context.user_data['complex_two'] = complex_two
        update.message.reply_text(
            f'Второе число {complex_two}, Выберите операцию с числами: \n\n+ - для сложения: \n - - для вычитания: \n * - для умножения: \n / - для деления: \n'
        )
        return OPERATIONS_COMPLEX
    else:
        update.message.reply_text('Это не то. Введите Re и Im второго числа через ПРОБЕЛ: ') 

def operations_complex(update, context):
    user = update.message.from_user
    logger.info("Пользователь выбрал операцию: %s: %s", user.first_name, update.message.text)
    complex_one = context.user_data.get('complex_one')
    complex_two = context.user_data.get('complex_two')
    user_choise = update.message.text
    if user_choise in '+-/*':
        if user_choise == '+':
            result = complex_one + complex_two
        if user_choise == '-':
            result = complex_one - complex_two
        if user_choise == '*':
            result = complex_one * complex_two
        if user_choise == '/':
            try:
                result = complex_one / complex_two
            except:
                update.message.reply_text('Деление на ноль запрещено')
        update.message.reply_text(
            f'Результат: {complex_one} + {complex_two} = {result}'
        )              
        return ConversationHandler.END
    else:
        update.message.reply_text('Это не то. Введите +-*/')        

def cancel(update, _):
    #определение пользователя
    user = update.message.from_user
    #Пишем в журнал о том, что пользователь не разговорчивый
    logger.info('Пользователь %s отменил разговор.', user.first_name)
    #отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        'Будет скучно - пиши.',
    )
    return CommandHandler.END

if __name__ == '__main__':
#Создаем Updater и передаем ему токен нашего бота
    updater = Updater('5667183654:AAEye6XpRN_v0Yc0ZUg0A_UA6OhdssFk_Y8')
    #ПОЛУЧАЕМ ДИСПЕТЧЕРА ДЛЯ РЕГИСТРАЦИИ ОБРАБОТЧИКОВ
    dispatcher = updater.dispatcher

    #определяем обработчик разговоров
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOISE: [MessageHandler(Filters.text, choise)],
            RATIONAL_ONE: [MessageHandler(Filters.text, rational_one)],
            RATIONAL_TWO: [MessageHandler(Filters.text, rational_two)],
            OPERATIONS_RATIONAL: [MessageHandler(Filters.text, operations_rational)],
            OPERATIONS_COMPLEX: [MessageHandler(Filters.text, operations_complex)
            ],     
            COMPLEX_ONE: [MessageHandler(Filters.text, complex_one)],
            COMPLEX_TWO: [MessageHandler(Filters.text, complex_two)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle


    












