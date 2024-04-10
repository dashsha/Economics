import matplotlib.pyplot as plt


#функция для создания графика общей КПВ
def kpv(A_1, B_1, A_2, B_2):
    # Создаем списки для точек A, B и C
    point_a = [A_1 + A_2, 0]
    point_b = [max(A_1, A_2), max(B_1, B_2)]
    point_c = [0, B_1 + B_2]

    #получение координат
    a_x, a_y = point_a
    b_x, b_y = point_b
    c_x, c_y = point_c

    #созданание графика
    plt.figure(figsize=(8, 6))
    plt.scatter([a_y, b_y, c_y], [a_x, b_x, c_x], color="blue", label="Точки")

    # Проводим отрезки через точки
    plt.plot([a_y, b_y], [a_x, b_x], color="blue",
             linestyle="--", label="Производитель 1")
    plt.plot([b_y, c_y], [b_x, c_x], color="green",
             linestyle="--", label="Производитель 2")

    # Добавление названий точкам
    plt.text(a_y, a_x, "A", fontsize=12, ha="right", va="bottom")
    plt.text(b_y, b_x, "B", fontsize=12, ha="left", va="top")
    plt.text(c_y, c_x, "C", fontsize=12, ha="right", va="top")

    #настройки графика
    plt.title("КПВ")
    plt.xlabel("Производство товара Б")
    plt.ylabel("Производство товара A")
    plt.legend()
    plt.grid(True)
    #сохранение графика в пнг
    plt.savefig("kpv.png")
    plt.close()


#функция для нахождения точки рыночного равновесия
def market_equilibrium(a, b, c, d):
    #получаем (P*) и объем (Q*)
    price = (a - c) / (d + b)
    value = a - b * price

    return price, value

#функция для расчеа объема дефицита/излишка для заданных функций спроса предложения и цены
def get_price_level_deficit_surplus(message, a1, b1, c1, d1):
    price_level = float(message.text)

    #считаем спрос и предложение
    demand = a1 - b1 * price_level
    supply = c1 + d1 * price_level
    #считаем разницу спроса и предложений
    deficit_or_surplus = demand - supply
    #выбираем нужное слово для ситуации на рынке
    if deficit_or_surplus > 0:
        situation = "дефицита"
    elif deficit_or_surplus < 0:
        situation = "излишка"
    else:
        situation = "равновесия"

    response = f"При уровне цены в {price_level} денежных единицах" \
               f" на рынке будет ситуация {situation}. Размер дефицита/излишка" \
               f" составит: {round(abs(deficit_or_surplus), 2)} единиц товара" \
               f" (при ситуации дефицита/излишка)"

    return response


#функция для рассчета прибыли фирмы
def profit_calculation(Q, P, costs):
    total_fixed_costs = sum(item[1] for item in costs["постоянные"])
    total_variable_costs = sum(item[1] for item in costs["переменные"])
    fixed_costs_sources = ", ".join(
        [f"{source[0]}, " \
         f"{source[1]} руб." for source in costs["постоянные"]]
    )

    variable_costs_sources = ", ".join(
        [
            f"{source[0]} ({source[1]} руб./единицу товара)"
            for source in costs["переменные"]
        ]
    )

    profit = Q * P - (total_variable_costs - total_fixed_costs)
    response = (
        f"При реализации {Q} единиц продукции по {P} руб. за единицу" \
        " товара и уровне "
        f"переменных издержек в {total_variable_costs} руб./единицу" \
        " товара "
        f"(включая: {variable_costs_sources}), "
        f"и постоянных издержек в {total_fixed_costs} руб. "
        f"(включая: {fixed_costs_sources}), прибыль составит:" \
        f" {round(profit, 2)} руб.")

    return response
