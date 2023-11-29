import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6980911495:AAHhKLiF0nvI40bdWEhiYIrfL2HxXxMWjBE",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Знакомство"  # Можно менять текст
text_button_1 = "Apple II"  # Можно менять текст
text_button_2 = "Apple II Plus"  # Можно менять текст
text_button_3 = "Apple III"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет, я расскажу тебе историю о компьютере Apple II, как тебя зовут?',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Супер! *Ваше* _имя_?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! *Ваш возраст?*')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за знакомство! \nПрочитай историю о компьютерах Apple по кнопкам меню!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Apple II - это первый персональный компьютер,  представленный в апреле 1977 года и серийно выпускавшийся компанией Apple Computer. Apple II был оснащен процессором MOS Technology 6502 с тактовой частотой 1 МГц, 4 КБ ОЗУ, 4 КБ ПЗУ, содержавшее монитор и интерпретатор Integer BASIC, интерфейсом для подключения кассетного магнитофона, графика монохромная 280×192 или цветная 140×192 в 4 или 6 цветов,работал на ОС Apple DOS", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "В июне 1979 года оригинальная модель была замещена моделью Apple II Plus, которая имела 48 КБ ОЗУ", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Apple III — это персональный компьютер для бизнеса, произведенный Apple Computer и выпущенный в 1980 году. Он имел процессор Synertek 6502A на частоте 2 МГц, оперативная память была 128 КБ, возможно увеличение до 512 КБ, работал на ОС Apple SOS", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

