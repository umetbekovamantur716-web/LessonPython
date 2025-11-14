

# Каждый тур имеет свою цену, длительность, статус (доступен/забронирован) и клиента, который его купил.
# Клиенты могут просматривать доступные туры, бронировать и оплачивать их.
# Агентство может смотреть общую выручку и управлять турами.

# 1. Класс Tour
# Инкапсулированный класс, представляющий один тур.
# Атрибуты:
# __id — уникальный номер тура (инкапсулированный, доступ только через свойство);
# __price — цена тура (инкапсулированный, управляется через @property);
# _is_booked — защищённый атрибут (True/False);
# _client — текущий клиент или None;
# _days — количество дней тура.

# Методы:
# book(client) — бронирует тур, делает его недоступным, если клиент оплатил.
# cancel_booking() — отменяет бронь, делает тур доступным.
# info() — краткая информация о туре.

# Свойства:
# price — через @property и @setter (цена не может быть ниже 5000 сом).
# id — только для чтения.

# 2. Класс Client
# Атрибуты:
# name — имя клиента;
# balance — баланс клиента.

# Методы:
# pay(amount) — уменьшает баланс, если хватает денег;
# add_balance(amount) — пополнение счёта;
# info() — возвращает строку с именем и балансом.


# 3. Класс Agency
# Атрибуты:
# name — название агентства;
# tours — список объектов Tour;
# _income — защищённый атрибут (доход агентства).

# Методы:
# add_tour(tour) — добавляет новый тур;
# show_available_tours() — показывает все свободные туры;
# book_tour(client, tour_id) — бронирует тур для клиента;
# cancel_all_bookings() — отменяет все активные брони;
# show_status() — показывает состояние всех туров и текущую выручку.


class Tour:
    # Конструктор: жаңы турду түзөт
    def __init__(self, tour_id, price, days):
        self.__id = tour_id       # уникалдуу номер (турду башка турлардан айырмалоо үчүн)
        self.__price = price      # баа (турдун наркын сактайт)
        self._is_booked = False   # брондолгонбу (True болсо, тур ээленген)
        self._client = None       # ким брондолгон (эч ким брондобогондо None болот)
        self._days = days         # турдун узактыгы күн менен (мисалы, 7 күн)
#1
    # __id үчүн property (тек гана окууга уруксат)
    @property
    def id(self):
        return self.__id          # турдун уникалдуу номерин кайтаруу

    # __price үчүн property (окуу жана жазуу)
    @property
    def price(self):
        return self.__price       # турдун баасын алуу

    @price.setter
    def price(self, new_price):
        if new_price > 0:         # баа 0 же терс болбошу керек
            self.__price = new_price  # бааны жаңыртуу

    # Турду брондоо функциясы
    def book(self, client_name):
        if not self._is_booked:           # эгер тур бош болсо
            self._is_booked = True        # турду брондолгон кылуу
            self._client = client_name    # ким брондолгонун сактоо

    # Тур тууралуу маалыматты көрсөтүү
    def info(self):
        status = "брондолгон" if self._is_booked else "бош"  # абалды текстке айлантуу
        client = self._client if self._client else "-"        # эгер эч ким брондобосо "-"
        print(f"ID:{self.__id}, Баасы:{self.__price}, Күндөрү:{self._days}, Абалы:{status}, Клиент:{client}")

#  2
class  Client:
    def __init__ (self, name, balance ):                         
        self.name = name 
        self.balance = balance
    def pay(self,amount):
        if amount <= self.balance: # эгер акча жетсе 
            self.balance -= amount  # Баланстан сумманы азайтуу
            return True             # Төлөө ийгиликтүү болду
        else:
            print("баланс жетишсиз ")
            return False
     # Баланска акча кошуу
    def add_balance(self, amount):
        if amount > 0:
            self.balance += amount   # Баланска сумманы кошуу

    # Клиент жөнүндө маалымат берүү
    def info(self):
        return f"Клиент: {self.name}, Баланс: {self.balance}"  # аты жана балансты кайтаруу 
# 3 
class Agency:
    # Конструктор: жаңы агентство түзөт
    def __init__(self, name):
        self.name = name          # Агентствонун аты
        self.tours = []           # Агентствонун бардык турлары (тизме)
        self._income = 0          # Агентствонун кирешеси (protected)

    # Жаңы тур кошуу
    def add_tour(self, tour):
        self.tours.append(tour)   # Тизмеге турду кошуу

    # Бош (available) турларды көрсөтүү
    def show_available_tours(self):
        print("Бош турлар:")
        for tour in self.tours:
            if not tour._is_booked:  # Эгер тур бош болсо
                tour.info()          # Тур тууралуу маалыматты көрсөтүү

    # Турду брондоо
    def book_tour(self, client, tour_id):
        for tour in self.tours:
            if tour.id == tour_id:         # Эгер ID дал келсе
                if not tour._is_booked:   # Эгер тур бош болсо
                    if client.pay(tour.price):  # Клиент төлөй алса
                        tour.book(client.name)  # Турду брондолгон кылуу
                        self._income += tour.price  # Кирешени кошуу
                        print(f"{client.name} турду брондоду!")
                    return
                else:
                    print("Бул тур мурунтан эле брондолгон!")
                    return
        print("Тур табылган жок!")  # Эгер ID жок болсо

    # Бардык брондорду жокко чыгаруу
    def cancel_all_bookings(self):
        for tour in self.tours:               
            if tour._is_booked:
                tour._is_booked = False   # Бронду жокко чыгаруу
                tour._client = None       # Клиентти жок кылуу
        print("Бардык брондор жокко чыгарылды.")

    # Турлар жана кирешени көрсөтүү
    def show_status(self):
        print(f"Турлар жана абал (Агентство: {self.name}):")
        for tour in self.tours:
            tour.info()                  # Ар бир тур тууралуу маалымат
        print(f"Жалпы киреше: {self._income}")  # Агентствонун кирешеси


    
