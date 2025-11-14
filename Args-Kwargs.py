# *args, ## **kwargs 

def add(*args):
    print(args)

add(7, 8, 5, 7, 8,4, ) 

a = [5, 6, 7, 8, 9,]
b = [1, 2, *a, 3, 4,]
print(b)


def sum2 (*args):
    total = 0 
    for n in args:
        total += n 
    print(f"сума :{total}")

sum2(4, 5, 6, 7, 8, 9, 357, )

def printScore(student, *args):
    print(f"Имя: {student}")
    for sc in args:
        print(sc, end= ', ')


printScore("Mao", 2, 2, 3, 4, 2, 3, )



##                       **kwargs KEYWORD ARGUMENTS - DICT { KEY:VALUE}

def  show(**kwargs):
    for k, v in kwargs.itmes():
        print(f"{k}: {v}")

show(name = 'Mao', age = 17, birth = '12.12.2000', city = 'Biskek')


def pets(owner, **kwargs):
    print(f"Хозяин: {owner}")
    for k, v in kwargs.itmes():
        print(k,v)

pets('Zahid', dog = 'bobik', cat = 'brubda', eats = ['fish', 'meat', 'water'])


# комбинаця
# оператор **kwargs нелзя писать до *args, если сделайте то будет ошибка 
# мы конечно не можем писать не только args т kwargs,  но и совсем другими словами, но общепрятые правила говорят чтобы писали именно так *args и **kwargs
def demo(*args, **kwargs):
    print('args=', args)
    print('kwargs=', kwargs)

demo(43,3, 4, 5, 6, 7, 56, 7, 8, 9, age = 45, hobbi = 'гимнастика',  phone = 'redmi')


