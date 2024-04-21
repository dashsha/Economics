from telebot import types
import telebot
import buttons
import solutions


#Максимальное колличество категорий
MAX_CATEGORIES = 5
costs = {"переменные": [], "постоянные": []}

bot = telebot.TeleBot("6871407282:AAEgC6qoSSV8ocO1PjvINJA2yXuesX9Uljg")


#обработка команды |start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Выберите что вы хотите рассчитать", reply_markup=buttons.main_keyboard())


#начало цикла заполнения переменных для рассчета точки рыночного равновесия
@bot.message_handler(func=lambda message: message.text == "Нахождение точки рыночного равновесия", content_types=["text"])
def market_equilibrium_start(message):
    bot.send_message(message.chat.id,"Значения это коэффициенты в формулах спроса и предложения: Qd=A-B*P и Qs=C+D*P",
        reply_markup=buttons.back_to_menu())
    bot.send_message(message.chat.id, "Введите переменную A:")

    bot.register_next_step_handler(message, get_coefficient_a_market_equilibrium)


#получение переменной А для рассчета точки рыночного равновесия
def get_coefficient_a_market_equilibrium(message):
    try:
        if message.text is not None:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            a = float(message.text)

            bot.send_message(message.chat.id, "Введите переменную B")
            bot.register_next_step_handler(message, get_coefficient_b_market_equilibrium, a)
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_a_market_equilibrium)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_a_market_equilibrium)


#получение переменной В для рассчета точки рыночного равновесия
def get_coefficient_b_market_equilibrium(message, a):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            b = float(message.text)

            bot.send_message(message.chat.id, "Введите переменную C")
            bot.register_next_step_handler(message, get_coefficient_c_market_equilibrium, a, b)
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_b_market_equilibrium, a)

    except ValueError:
        bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_b_market_equilibrium, a)


#получение переменной С для рассчета точки рыночного равновесия
def get_coefficient_c_market_equilibrium(message, a, b):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            c = float(message.text)

            bot.send_message(message.chat.id, "Введите коэффициент D:")
            bot.register_next_step_handler(message, get_coefficient_d_market_equilibrium, a,b,c)
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_c_market_equilibrium, a, b)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_c_market_equilibrium,a, b)

#получение переменной D для рассчета точки рыночного равновесия
def get_coefficient_d_market_equilibrium(message, a, b, c):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            d = float(message.text)

            try:
                price, value = solutions.market_equilibrium(a, b, c, d)

                response = f"Рыночное равновесие:\nЦена (P*): {round(price, 2)}\nОбъем (Q*): {round(value)}"
                bot.send_message(message.chat.id, response)

            except ZeroDivisionError:
                bot.send_message(message.chat.id, "Ошибка: Деление на ноль невозможно")
                handle_back_to_menu_button(message)

        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_d_market_equilibrium, a, b, c)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_d_market_equilibrium, a, b, c)


#начало цикла заполнения переменных для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
@bot.message_handler(func=lambda message: message.text == "Расчет объема дефицита/излишка для заданных функций спроса предложения и цены", content_types=["text"])
def handle_deficit_or_surplus_calculation_start(message):
    #очищаем клавиатуру
    types.ReplyKeyboardRemove()

    bot.send_message(
        message.chat.id, "Переменные являются коэффициентами в соответствующих функциях спроса и предложения: Qd = A - B*P. Qs = C + D*P.",
        reply_markup=buttons.back_to_menu())

    bot.send_message(message.chat.id, "Введите переменную A")
    bot.register_next_step_handler(message, get_coefficient_a_deficit_surplus)


#получение переменной А для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
def get_coefficient_a_deficit_surplus(message):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            a1 = float(message.text)

            bot.send_message(message.chat.id, "Введите переменную B:")
            bot.register_next_step_handler(message, get_coefficient_b_deficit_surplus, a1)
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_a_deficit_surplus)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_a_deficit_surplus)


#получение переменной В для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
def get_coefficient_b_deficit_surplus(message, a1):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            b1 = float(message.text)

            bot.send_message(message.chat.id, "Введите коэффициент C:")
            bot.register_next_step_handler(message, get_coefficient_c_deficit_surplus, a1, b1)
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_b_deficit_surplus, a1)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_b_deficit_surplus, a1)


#получение переменной С для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
def get_coefficient_c_deficit_surplus(message, a1, b1):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            c1 = float(message.text)

            bot.send_message(message.chat.id, "Введите коэффициент D:")
            bot.register_next_step_handler(message, get_coefficient_d_deficit_surplus,a1, b1, c1)

        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_c_deficit_surplus, a1, b1)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message,get_coefficient_c_deficit_surplus, a1, b1)


#получение переменной D для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
def get_coefficient_d_deficit_surplus(message, a1, b1, c1):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            d1 = float(message.text)

            bot.send_message(message.chat.id, "Введите цену Е")
            bot.register_next_step_handler(message, get_price_level_deficit_surplus, a1, b1, c1, d1)

        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_coefficient_d_deficit_surplus, a1, b1, c1)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_coefficient_d_deficit_surplus, a1, b1, c1)


#получение переменной Цены для расчета объема дефицита/излишка для заданных функций спроса предложения и цены
def get_price_level_deficit_surplus(message, a1, b1, c1, d1):
    try:
        if message.text is not None:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            price_level = float(message.text)

            if price_level < 0:
                bot.send_message(message.chat.id,"Можно указать только положительную переменную цены")
                bot.register_next_step_handler(message, get_price_level_deficit_surplus, a1, b1, c1, d1,)
                return

            response = solutions.get_price_level_deficit_surplus(message, a1, b1, c1, d1)
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_price_level_deficit_surplus, a1, b1, c1, d1)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_price_level_deficit_surplus,a1, b1, c1, d1)


#Начало цикла обработки расчета прибыли фирмы
@bot.message_handler(func=lambda message: message.text == "Расчет прибыли фирмы", content_types=["text"])
def handle_profit_calculation_start(message):
    if message:
        #очищение клавиатуры
        types.ReplyKeyboardRemove()

        if message.text == "Назад":
            handle_back_to_menu_button(message)
            return

        bot.send_message(message.chat.id, "Для расчета прибыли фирмы введите следующие данные:", reply_markup=buttons.back_to_menu())
        bot.send_message(message.chat.id, "Объем производства в штуках Q")
        bot.register_next_step_handler(message, get_production_volume)


#Получение объема производства
def get_production_volume(message):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            Q = int(message.text)

            if Q < 0:
                bot.send_message(message.chat.id, "Для объема производства принимаются только положительные числа")
                bot.register_next_step_handler(message, get_production_volume)
                return

            bot.send_message(message.chat.id, "Цена за единицу товара P")
            bot.register_next_step_handler(message, get_unit_price, Q)
        else:
            bot.send_message(message.chat.id, "Принимаются только положительные числа")
            bot.register_next_step_handler(message, get_production_volume)

    except ValueError:
        bot.send_message(message.chat.id, "Принимаются только положительные числа")
        bot.register_next_step_handler(message, get_production_volume)


#получение цены за штуку
def get_unit_price(message, Q):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            P = float(message.text)

            if P < 0:
                bot.send_message(message.chat.id,"Для цены за единицу товара примнимаются только положительные числа")
                bot.register_next_step_handler(message, get_unit_price, Q)
                return

            bot.send_message(
                message.chat.id,
                f"Постоянные издержки FC" \
                f" введите данные в формате 'Название" \
                f" издержки, размер издержки'. (введите" \
                f" 'готово' для завершения, максимум {MAX_CATEGORIES} издержек):",
            )
            bot.register_next_step_handler(message, get_fixed_costs, Q, P)

        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_unit_price, Q)

    except ValueError:
        bot.send_message(message.chat.id, "Для цены за единицу товара примнимаются только положительные числа")
        bot.register_next_step_handler(message, get_unit_price, Q)


#получение издерждек
def get_fixed_costs(message, Q, P):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            if message.text.lower() == "готово":
                bot.send_message(
                    message.chat.id,
                    f"Переменные издержки VC" \
                    f" введите данные в формате 'Название издержки, размер" \
                    f" издержки'.  (введите 'готово'" \
                    f" для завершения, максимум {MAX_CATEGORIES} издержек):",
                )
                bot.register_next_step_handler(message, get_variable_costs, Q, P)

            else:
                handle_costs_input(message, Q, P, "постоянные")
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_fixed_costs, Q, P)

    except ValueError:
        bot.send_message(message.chat.id, "Для цены за единицу издержки можно использовать только положительные числа")
        bot.register_next_step_handler(message, get_fixed_costs, Q, P)


#получение издержек
def get_variable_costs(message, Q, P):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            if message.text.lower() == "готово":
                response = solutions.profit_calculation(Q, P, costs)
                bot.send_message(message.chat.id, response)

            else:
                handle_costs_input(message, Q, P, "переменные")
        else:
            bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_variable_costs, Q, P)

    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Введите числовое значение для цены за единицу и.")
        bot.register_next_step_handler(message, get_variable_costs, Q, P)


#обработка списка издержек
def handle_costs_input(message, Q, P, cost_type):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            input_costs = message.text.split(", ")
            name, cost = input_costs[0], float(input_costs[1])

            if cost < 0:
                bot.send_message(message.chat.id, "Для издержек можно ввести только положительное число")
                bot.register_next_step_handler(message, handle_costs_input, Q, P, cost_type)
                return

            if len(costs[cost_type]) < MAX_CATEGORIES:
                costs[cost_type].append((name, cost))
                bot.send_message(message.chat.id,f"Добавлены {cost_type} издержки: {name}, {cost}\nВведите следующие или 'Готово'.")
                if cost_type == "постоянные":
                    bot.register_next_step_handler(message, get_fixed_costs, Q, P)
                else:
                    bot.register_next_step_handler(message, get_variable_costs, Q, P)
            else:
                bot.send_message(message.chat.id, f"Больше нельзя вводить издержки. Достингнуто максимальное колличство\nВведите 'Готово'.")
                if cost_type == "постоянные":
                    bot.register_next_step_handler(message, get_fixed_costs, Q, P)
                else:
                    bot.register_next_step_handler(message, get_variable_costs, Q, P)
        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, handle_costs_input)

    except (ValueError, IndexError):
        bot.send_message(message.chat.id,"Некорректный ввод. Пожалуйста, введите данные так: 'Название издержки, размер издержки'.")
        if cost_type == "постоянные":
            bot.register_next_step_handler(message, get_fixed_costs, Q, P)
        else:
            bot.register_next_step_handler(message, get_variable_costs, Q, P)


#обработки кнопки назад
@bot.message_handler(func=lambda message: message.text.lower() == "назад")
def handle_back_to_menu_button(message):
    bot.send_message(message.chat.id, "Выберите опцию:",
                     reply_markup=buttons.main_keyboard())


# Обработчик нажатия на кнопку "Построение общей КПВ"
@bot.message_handler(func=lambda message: message.text == "Построение общей КПВ")
def handle_build_kpv(message):
    #очистка клавиатуры
    types.ReplyKeyboardRemove()

    bot.send_message(message.chat.id, "Введите максимальный объем производства товара А для производителя 1:", reply_markup=buttons.back_to_menu())
    bot.register_next_step_handler(message, get_max_production_a1)


#получение максимального объема производства для товара А и производителя 1
def get_max_production_a1(message):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            max_production_a1 = float(message.text)

            while max_production_a1 < 0:
                bot.send_message(
                    message.chat.id,
                    "Пожалуйста, введите неотрицательное числовое" \
                    " значение для максимального объема производства" \
                    " товара А для производителя 1:",
                )
                bot.register_next_step_handler(message, get_max_production_a1)
                return

            bot.send_message(message.chat.id, "Введите максимальный объем производства товара Б для производителя 1:")
            bot.register_next_step_handler(message, get_max_production_b1, max_production_a1)

        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_max_production_a1)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_max_production_a1)


#получение максимального объема производства для товара В и производителя 1
def get_max_production_b1(message, max_production_a1):
    try:
        if message.text :
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            max_production_b1 = float(message.text)

            while max_production_b1 < 0:
                bot.send_message(message.chat.id, "Требуется положительное число")
                bot.register_next_step_handler(message, get_max_production_b1, max_production_a1)
                return

            bot.send_message(message.chat.id,"Введите максимальный объем производства товара А для производителя 2:")
            bot.register_next_step_handler(message, get_max_production_a2, max_production_a1, max_production_b1)

        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_max_production_b1, max_production_a1)

    except ValueError:
        bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_max_production_b1, max_production_a1)


#получение максимального объема производства для товара А и производителя 2
def get_max_production_a2(message, max_production_a1, max_production_b1):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            max_production_a2 = float(message.text)
            while max_production_a2 < 0:
                bot.send_message(message.chat.id, "Требуется положительное число")
                bot.register_next_step_handler(message, get_max_production_a2, max_production_a1, max_production_b1)
                return

            bot.send_message(message.chat.id, "Введите максимальный объем производства товара Б для производителя 2:")

            bot.register_next_step_handler(message, get_max_production_b2, max_production_a1, max_production_b1, max_production_a2)

        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_max_production_a2, max_production_a1, max_production_b1)

    except ValueError:
        bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message, get_max_production_a2, max_production_a1, max_production_b1)


#получение максимального объема производства для товара В и производителя 2
def get_max_production_b2(message, max_production_a1, max_production_b1, max_production_a2):
    try:
        if message.text:
            if message.text == "Назад":
                handle_back_to_menu_button(message)
                return

            max_production_b2 = float(message.text)
            while max_production_b2 < 0:
                bot.send_message(message.chat.id, "Требуется положительное число")
                bot.register_next_step_handler(message, get_max_production_b2, max_production_a1, max_production_b1, max_production_a2)
                return

            # Построение графика общей КПВ
            solutions.kpv(max_production_a1, max_production_b1, max_production_a2, max_production_b2)

            bot.send_photo(message.chat.id, open("kpv.png", "rb"))

        else:
            bot.send_message(message.chat.id,"Неверный ввод. Принимаются только числа")
            bot.register_next_step_handler(message, get_max_production_b2, max_production_a1, max_production_b1, max_production_a2)

    except ValueError:
        bot.send_message(message.chat.id, "Неверный ввод. Принимаются только числа")
        bot.register_next_step_handler(message,get_max_production_b2, max_production_a1, max_production_b1, max_production_a2)


bot.polling(none_stop=True)
