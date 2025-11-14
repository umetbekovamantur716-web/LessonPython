
# Требуется реализовать систему управления книжным магазином с использованием инкапсуляции, наследования, аргументов *args и **kwargs.
# класс BaseBook:
# защищённые атрибуты: _title, _author
# приватный атрибут: __price
# свойство price с проверкой (цена ≥ 100)
# абстрактный метод info()
# Классы-наследники от BaseBook:
# • Book — обычная книга. Реализация info(): «Книга: <title> — <author>, <price> сом»
# • EBook — электронная книга. Доп. атрибут: _file_size_mb. info(): «Электронная книга: <title> — <author>, <price> сом, файл <size> МБ»
# • AudioBook — аудиокнига. Доп. атрибут: _duration_min. info(): «Аудиокнига: <title> — <author>, <price> сом, длительность <minutes> мин»
# Класс Inventory (склад):
# защищённый список _books
# метод add_books(*books): принимает любое количество объектов книг, проверяет тип
# метод find_books(**filters): возвращает список книг, соответствующих переданным параметрам
# метод remove_book(book): удаляет книгу
# метод all_books(): возвращает копию списка книг
# Класс BookStore:
# атрибут name
# объект inventory
# приватный атрибут __income + свойство income (только чтение)
# метод sell_book(title): ищет по названию, удаляет книгу, увеличивает доход
# метод show_status(): возвращает название магазина, доход и список всех книг через info()
# Требования:
# обязательно использовать инкапсуляцию (__ и _), наследование, полиморфизм, *args, **kwargs
# система должна демонстрировать добавление книг, поиск, продажу и отображение состояния магазина
class BaseBook:
    def __init__(self, title, author, price):
        self._title = title
        self._author = author
        self.__price = price
    
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value >= 100:
            self.__price = value

    def info(self):
        return f"{self._title} {self._author} {self.price}"
    
class Book(BaseBook):
    def info(self):
        return f"Книга:{self._title} автор:{self._author} {self.price}сом"

class EBook(BaseBook):
    def __init__(self, title, author, price, file_size_mb):
        super().__init__(title, author, price)
        self._file_size_mb = file_size_mb
    
    def info(self):
        return f"«Электронная книга:{self._title} автор:{self._author} {self.price}сом, файл {self._file_size_mb} МБ"

class AudioBook(BaseBook):
    def __init__(self, title, author, price, duration_min):
        super().__init__(title, author, price)
        self._duration_min = duration_min
    
    def info(self):
        return f"«Электронная книга:{self._title} автор:{self._author} {self.price}сом, длительность {self._duration_min} МБ"
    
class Inventory:
    def __init__(self):
        self._books = []

    def add_books(self, *books): #принимает любое количество объектов книг
        for book in books:
            self._books.append(book)

    def find_books(self, **filters): #возвращает список книг
        res = self._books
        for key, value in filters.items():
            res = [b for b in res if getattr(b, f"_{key}", None) == value]
        return res 
    
    def remove_book(self, book): #удаляет книгу
        if book in self._books:
            self._books.remove(book)

    def all_books(self): #возвращает копию списка книг
        return self._books.copy()
    
class BookStore:
    def __init__(self, name):
        self.name = name 
        self.inventory = Inventory() 
        self.__income = 0 # доход нашего магазина
    
    @property
    def income(self):
        return self.__income
    
    #ищет по названию, удаляет книгу, увеличивает доход
    def sell_book(self, title): 
        for book in self.inventory.all_books():
            if book._title  == title:
                self.__income += book.price
                self.inventory.remove_book(book)
                return True
        return False

    #возвращает название магазина, доход и список всех книг через info()
    def show_status(self): 
        return {
            'магазин': self.name,
            'Доход': self.__income,
            'Книги': [b.info() for b in self.inventory.all_books()]
        }

b1 = Book('Преступление и наказание', "Достоевский", 500)
b2 = EBook('Грокаем алгоритмы', "А. Бхаргава", 700, file_size_mb=20)
b3 = AudioBook('Python машинное обучение', "Гена", 300, duration_min=700)

store = BookStore('Айтишная Лайб')
store.inventory.add_books(b1,b2,b3)
found = store.inventory.find_books(author='Достоевский')
for book in found:
    print(book.info())

store.sell_book('Грокаем алгоритмы')
print(store.show_status())