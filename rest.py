
# ЗАДАЧА: «Система управления рестораном»
# Требуется разработать систему моделирования работы ресторана, используя инкапсуляцию, наследование, полиморфизм, а также *args и **kwargs.
# защищённые атрибуты: _name, _quantity (в граммах)
# приватный атрибут: __price_per_gram
# свойство price_per_gram (цена ≥ 0.1)
# метод cost(weight): возвращает стоимость weight граммов

# Класс Dish (базовый класс для всех блюд):
# защищённые атрибуты: _name, _ingredients (словарь: ингредиент → граммы)
# приватный атрибут: __base_price (минимум 20 сом, через свойство)
# метод total_cost(): стоимость ингредиентов + base_price
# метод info(): будет переопределён в наследниках

# Наследники Dish:
# • HotDish — горячее блюдо
# Доп. атрибут: _spicy_level (0–5)
# info(): «Горячее блюдо: <name>, острота <spicy>, цена <total_cost>»
# • Dessert — десерт
# Доп. атрибут: _sweetness (0–10)
# info(): «Десерт: <name>, сладость <sweetness>, цена <total_cost>»
# • Drink — напиток
# Доп. атрибут: _volume_ml
# info(): «Напиток: <name>, объем <volume> мл, цена <total_cost>»

# Класс Kitchen:
# защищённый список _dishes
# метод add_dishes(*dishes): принимает любое количество блюд
# метод find_dishes(**filters): поиск по любым параметрам (name, spicy_level, sweetness и т.д.)
# метод remove_dish(dish)
# метод all_dishes(): возврат копии списка

# Класс Restaurant:
# атрибут name
# объект kitchen
# приватный атрибут __income (через свойство только чтение)
# метод order_dish(dish_name): продаёт блюдо, увеличивает доход, убирает из меню
# метод menu(): список всех блюд через info()
# метод status(): доход и количество оставшихся блюд 

from copy import deepcopy
from typing import Dict, Any, Iterable, Tuple


class Ingredient:
    """Ингредиент: защищённые _name, _quantity (в граммах), приватный __price_per_gram."""
    def __init__(self, name: str, quantity: float, price_per_gram: float):
        self._name = str(name)
        self._quantity = float(quantity)
        self.__price_per_gram = None
        self.price_per_gram = price_per_gram  # через свойство (валидация)

    @property
    def price_per_gram(self) -> float:
        return self.__price_per_gram

    @price_per_gram.setter
    def price_per_gram(self, value: float):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError("price_per_gram must be a number")
        if value < 0.1:
            raise ValueError("price_per_gram must be >= 0.1")
        self.__price_per_gram = value

    def cost(self, weight: float) -> float:
        """Стоимость weight грамм этого ингредиента."""
        weight = float(weight)
        if weight < 0:
            raise ValueError("weight must be non-negative")
        return weight * self.__price_per_gram

    def __repr__(self):
        return f"Ingredient({self._name!r}, {self._quantity}g, {self.__price_per_gram}/g)"


class Dish:
    """
    Базовый класс Dish.
    _name, _ingredients: dict(Ingredient -> grams)
    приватный __base_price (через свойство, минимум 20)
    """
    def __init__(self, name: str, ingredients: Dict[Ingredient, float], base_price: float = 20.0, **kwargs):
        self._name = str(name)
        # ожидаем ingredients: {Ingredient: grams, ...}
        self._ingredients = {}
        for ing, grams in ingredients.items():
            if not isinstance(ing, Ingredient):
                raise TypeError("keys of ingredients must be Ingredient instances")
            grams = float(grams)
            if grams < 0:
                raise ValueError("ingredient grams must be non-negative")
            self._ingredients[ing] = grams

        self.__base_price = None
        self.base_price = base_price  # через свойство с валидацией

        # allow subclasses to pass extra kwargs (используется для *args/**kwargs демонстрации)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def base_price(self) -> float:
        return self.__base_price

    @base_price.setter
    def base_price(self, value: float):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError("base_price must be a number")
        if value < 20.0:
            raise ValueError("base_price must be at least 20.0")
        self.__base_price = value

    def total_cost(self) -> float:
        """сумма стоимости всех ингредиентов (по указанным граммам) + base_price"""
        ingredients_cost = 0.0
        # суммируем cost каждого ингредиента (ingredient.cost(grams))
        for ing, grams in self._ingredients.items():
            ingredients_cost += ing.cost(grams)
        return ingredients_cost + self.__base_price

    def info(self) -> str:
        """Базовая заглушка — наследники переопределяют."""
        return f"Блюдо: {self._name}, цена {self.total_cost():.2f}"

    def __repr__(self):
        return f"<Dish {self._name}>"

    @property
    def name(self):
        return self._name


class HotDish(Dish):
    def __init__(self, name: str, ingredients: Dict[Ingredient, float], spicy_level: int = 0, base_price: float = 20.0, **kwargs):
        super().__init__(name, ingredients, base_price=base_price, **kwargs)
        if not isinstance(spicy_level, int):
            raise TypeError("spicy_level must be int")
        if not (0 <= spicy_level <= 5):
            raise ValueError("spicy_level must be between 0 and 5")
        self._spicy_level = spicy_level

    def info(self) -> str:
        return f"Горячее блюдо: {self._name}, острота {self._spicy_level}, цена {self.total_cost():.2f}"


class Dessert(Dish):
    def __init__(self, name: str, ingredients: Dict[Ingredient, float], sweetness: int = 0, base_price: float = 20.0, **kwargs):
        super().__init__(name, ingredients, base_price=base_price, **kwargs)
        if not isinstance(sweetness, int):
            raise TypeError("sweetness must be int")
        if not (0 <= sweetness <= 10):
            raise ValueError("sweetness must be between 0 and 10")
        self._sweetness = sweetness

    def info(self) -> str:
        return f"Десерт: {self._name}, сладость {self._sweetness}, цена {self.total_cost():.2f}"


class Drink(Dish):
    def __init__(self, name: str, ingredients: Dict[Ingredient, float], volume_ml: float = 250.0, base_price: float = 20.0, **kwargs):
        super().__init__(name, ingredients, base_price=base_price, **kwargs)
        volume_ml = float(volume_ml)
        if volume_ml <= 0:
            raise ValueError("volume_ml must be positive")
        self._volume_ml = volume_ml

    def info(self) -> str:
        return f"Напиток: {self._name}, объем {self._volume_ml:.0f} мл, цена {self.total_cost():.2f}"


class Kitchen:
    """Kitchen: защищённый список _dishes, методы add_dishes, find_dishes, remove_dish, all_dishes."""
    def __init__(self):
        self._dishes = []

    def add_dishes(self, *dishes: Dish):
        """Добавляет любое количество блюд (использует *args)."""
        for d in dishes:
            if not isinstance(d, Dish):
                raise TypeError("only Dish instances can be added")
            self._dishes.append(d)

    def find_dishes(self, **filters) -> list:
        """
        Поиск блюд по любым параметрам.
        Поддерживает:
         - точное совпадение для строк/чисел (name="Tea")
         - диапазон для чисел через tuple/list (min, max)
        Проверяет: публичные атрибуты, защищённые (_attr) и свойства.
        """
        results = []
        for d in self._dishes:
            match = True
            for key, expected in filters.items():
                # пытаемся получить значение через разные варианты именования
                value = getattr(d, key, None)
                if value is None:
                    value = getattr(d, f"_{key}", None)
                if value is None:
                    # поддержка для 'name' как special-case
                    if key == "name":
                        value = getattr(d, "name", None)
                if value is None:
                    match = False
                    break

                # если фильтр — диапазон (tuple/list of length 2)
                if isinstance(expected, (tuple, list)) and len(expected) == 2 and all(isinstance(x, (int, float)) for x in expected):
                    min_v, max_v = expected
                    try:
                        num = float(value)
                        if not (min_v <= num <= max_v):
                            match = False
                            break
                    except (TypeError, ValueError):
                        match = False
                        break
                else:
                    # точное сравнение (строки — нечувствительное к регистру)
                    if isinstance(expected, str) and isinstance(value, str):
                        if expected.lower() != value.lower():
                            match = False
                            break
                    else:
                        if value != expected:
                            match = False
                            break

            if match:
                results.append(d)
        return results

    def remove_dish(self, dish: Dish):
        """Удаляет блюдо из кухни (если есть)."""
        try:
            self._dishes.remove(dish)
            return True
        except ValueError:
            return False

    def all_dishes(self) -> list:
        """Возвращает копию списка блюд."""
        return deepcopy(self._dishes)

    def __repr__(self):
        return f"<Kitchen: {len(self._dishes)} dishes>"


class Restaurant:
    """Restaurant: name, kitchen, приватный __income (только чтение), методы order_dish, menu, status."""
    def __init__(self, name: str, kitchen: Kitchen):
        self.name = str(name)
        if not isinstance(kitchen, Kitchen):
            raise TypeError("kitchen must be a Kitchen instance")
        self.kitchen = kitchen
        self.__income = 0.0

    @property
    def income(self) -> float:
        """Только чтение приватного дохода."""
        return self.__income

    def order_dish(self, dish_name: str) -> Tuple[bool, str]:
        """
        Продаёт блюдо по имени: ищет первое совпадение, добавляет к доходу total_cost,
        удаляет блюдо из кухни и возвращает (True, сообщение). Если не найдено — (False, msg).
        """
        candidates = self.kitchen.find_dishes(name=dish_name)
        if not candidates:
            return False, f"Блюдо с именем '{dish_name}' не найдено."
        dish = candidates[0]
        cost = dish.total_cost()
        # увеличить доход
        self.__income += cost
        # удалить блюдо из кухни (предполагается, что блюдо единичная порция)
        removed = self.kitchen.remove_dish(dish)
        if not removed:
            return False, f"Не удалось удалить блюдо '{dish_name}' из кухни."
        return True, f"Продано '{dish_name}', цена {cost:.2f}. Текущий доход: {self.__income:.2f}"

    def menu(self) -> list:
        """Возвращает список info() для всех блюд."""
        return [d.info() for d in self.kitchen.all_dishes()]

    def status(self) -> str:
        """Возвращает строку со статусом: доход и количество блюд."""
        return f"Доход: {self.__income:.2f}, блюд в меню: {len(self.kitchen.all_dishes())}"

    def __repr__(self):
        return f"<Restaurant {self.name}: income={self.__income:.2f}>"


# ----------------------------
# Пример использования / демонстрация
# ----------------------------
if __name__ == "__main__":
    # создаём ингредиенты
    rice = Ingredient("Rice", 10000, price_per_gram=0.05)   # дешевый (но price_per_gram минимум 0.1 — валидация запрещает меньше)
    # поправим: пример верный — используем >=0.1
    rice = Ingredient("Rice", 10000, price_per_gram=0.1)
    meat = Ingredient("Meat", 5000, price_per_gram=1.5)
    sugar = Ingredient("Sugar", 2000, price_per_gram=0.2)
    milk = Ingredient("Milk", 5000, price_per_gram=0.5)
    tea_leaf = Ingredient("TeaLeaf", 1000, price_per_gram=2.0)

    # создаём блюда (каждый ингредиент с указанием граммов для этого блюда)
    plov = HotDish(
        "Plov",
        ingredients={rice: 200.0, meat: 150.0},
        spicy_level=2,
        base_price=50.0
    )

    cake = Dessert(
        "Honey Cake",
        ingredients={sugar: 100.0, milk: 200.0},
        sweetness=8,
        base_price=40.0
    )

    tea = Drink(
        "Green Tea",
        ingredients={tea_leaf: 5.0, milk: 50.0},
        volume_ml=300.0,
        base_price=20.0
    )

    # кухню и ресторан
    kitchen = Kitchen()
    kitchen.add_dishes(plov, cake, tea)

    rest = Restaurant("MyRestaurant", kitchen)

    # меню
    print("=== MENU ===")
    for line in rest.menu():
        print(line)

    # статус
    print("\n" + rest.status())

    # найти острые блюда (spicy_level >= 1)
    spicy = kitchen.find_dishes(spicy_level=(1, 5))
    print("\nSpicy dishes:")
    for d in spicy:
        print(d.info())

    # сделать заказ
    ok, msg = rest.order_dish("Plov")
    print("\nOrder:", msg)

    # статус после продажи
    print("\n" + rest.status())

    # меню после продажи
    print("\n=== MENU AFTER ===")
    for line in rest.menu():
        print(line)

        