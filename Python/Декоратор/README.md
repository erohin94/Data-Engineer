# **Декоратор**

**Декоратор в Python** — это функция, которая принимает другую функцию и расширяет её функциональность, не изменяя её код. Декораторы часто используются для добавления дополнительной логики, например, для логирования, проверки прав доступа, измерения времени выполнения и так далее.

Пример простого декоратора, который выводит сообщение до и после выполнения функции:

```
# Определение декоратора
def my_decorator(func):
    def wrapper():
        print("До выполнения функции")
        func()
        print("После выполнения функции")
    return wrapper

# Применение декоратора
@my_decorator
def say_hello():
    print("Привет!")

# Вызов декорированной функции
say_hello()
```

Вывод:

```
До выполнения функции
Привет!
После выполнения функции
```

`my_decorator` — это декоратор, который принимает функцию func в качестве аргумента.

Внутри `my_decorator` создаётся функция `wrapper()`, которая вызывает `func()` и добавляет дополнительную логику (выводит сообщения до и после вызова функции).

Символ `@my_decorator` перед функцией say_hello() применяет декоратор к этой функции.

Когда вызывается `say_hello()`, фактически выполняется `wrapper()`, и в процессе этого вызывается исходная функция с добавленной логикой.

# **Декоратор для измерения времени выполнения функции**

```
import time

# Декоратор для измерения времени выполнения
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        lst = []
        start_time = time.time()  # Засекаем время начала
        result = func(*args, **kwargs)  # Вызываем исходную функцию
        end_time = time.time()  # Засекаем время окончания
        print(f"Время выполнения функции {func.__name__}: {end_time - start_time:.4f} секунд")
        lst.append(f"Время старата: {start_time} - Время окончания {end_time}")
        return lst
    return wrapper

# Применение декоратора
@timer_decorator
def slow_function():
    print("Отсчет пошел")
    time.sleep(2)  # Эмуляция долгой работы

slow_function()

----------------------------------------------------------
Отсчет пошел
Время выполнения функции slow_function: 2.0002 секунд
['Время старата: 1742373674.2935667 - Время окончания 1742373676.2937737']
```

Этот декоратор измеряет время до и после выполнения функции и выводит разницу.

Он принимает произвольные аргументы `*args` и `**kwargs`, чтобы работать с функциями, которые могут принимать параметры.

Вызов `slow_function()` будет выводить время, затраченное на выполнение функции.

# **Декоратор с параметрами**

**Структура проекта:**

project/
├── hh_templates.py    ← здесь декоратор и функция
└── data_for_model.py    ← здесь вызываем и передаём переменные

**Файл 1: hh_templates.py**

```
def split_area_decorator(df_handbook, df_handbook_id):
    def decorator(func):
        def wrapper():
            print("Декоратор сработал")
            print("df_handbook:", df_handbook)
            print("df_handbook_id:", df_handbook_id)
            templates = func()

            # Пример: добавим регион в каждый шаблон
            new_templates = []
            for template in templates:
                for region_id in df_handbook_id:
                    t = template.copy()
                    t['region_id'] = region_id
                    new_templates.append(t)
            return new_templates
        return wrapper
    return decorator


def hh_search_templates():
    """
    Просто возвращает базовые шаблоны.
    """
    templates = [
                {"name": "Data Scientist", "keywords": ["ML", "AI"]},
                {"name": "Backend Developer", "keywords": ["Python", "Django"]}
                ]
    return templates
```

**Файл 2: data_for_model.py**

```
# data_for_model.py
from hh_templates import hh_search_templates as base_templates, split_area_decorator

# Пример переменных
df_handbook = "Это справочник" 
df_handbook_id = [1, 2, 3]

# Оборачиваем функцию с параметрами
hh_search_templates = split_area_decorator(df_handbook, df_handbook_id)(base_templates)

# Вызываем
result = hh_search_templates()

# Печатаем результат
for item in result:
    print(item)
```

```
PS C:\Users\erohi\Desktop\gazprombank\test_decorator> python data_for_model.py
Декоратор сработал
df_handbook: Это справочник
df_handbook_id: [1, 2, 3]
{'name': 'Data Scientist', 'keywords': ['ML', 'AI'], 'region_id': 1}
{'name': 'Data Scientist', 'keywords': ['ML', 'AI'], 'region_id': 2}
{'name': 'Data Scientist', 'keywords': ['ML', 'AI'], 'region_id': 3}
{'name': 'Backend Developer', 'keywords': ['Python', 'Django'], 'region_id': 1}
{'name': 'Backend Developer', 'keywords': ['Python', 'Django'], 'region_id': 2}
{'name': 'Backend Developer', 'keywords': ['Python', 'Django'], 'region_id': 3}
```
В `hh_templates.py` не оборачиваем функцию — экспортируем её «чистой».

`В data_for_model.py`:

Импортируем базовую функцию

Передаём справочник и ID

Оборачиваем её с декоратором с параметрами





