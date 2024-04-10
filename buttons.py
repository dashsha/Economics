from telebot import types


#клавиатура для возврщаения в меню
def back_to_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton("Назад")
    keyboard.add(button)
    return keyboard


#клавиатура главного меню
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    kpv_button = types.KeyboardButton("Построение общей КПВ")
    market_equilibrium_button = types.KeyboardButton("Нахождение точки рыночного равновесия")
    deficit_surplus_button = types.KeyboardButton("Расчет объема дефицита/излишка для заданных функций спроса предложения и цены")
    profit_calc_button = types.KeyboardButton("Расчет прибыли фирмы")

    keyboard.add(kpv_button, market_equilibrium_button, deficit_surplus_button, profit_calc_button)

    return keyboard
