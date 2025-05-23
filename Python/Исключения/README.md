# **Исключения**

# **try - except**

Конструкция `try...except` используется для обработки исключений (ошибок), чтобы предотвратить остановку программы из-за непредвиденных ситуаций. 

Внутри блока `try` размещается код, который может вызвать исключение, а в блоке `except` — обработчик этого исключения. 

**Пример**

Если значение `b` равно 0, возникает ошибка `ZeroDivisionError`, и тогда блок `except` перехватывает это исключение и возвращает строку "Ошибка: деление на ноль!".

```
def divide(a, b):
    try:
        result = a / b  # попытка выполнить деление
        return result   # если деление успешно, возвращаем результат
    except ZeroDivisionError:
        return "Ошибка: деление на ноль!"  # если делитель равен нулю, возвращаем сообщение об ошибке

# Пример вызова функции
print(divide(10, 2))  # Результат: 5.0
print(divide(10, 0))  # Результат: Ошибка: деление на ноль!

-------------------------------------------------------------
5.0
Ошибка: деление на ноль!
```

**Пример 2**

```
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Ошибка: деление на ноль!"
    except TypeError:
        return "Ошибка: неверный тип данных!"
    
print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # Ошибка: деление на ноль!
print(safe_divide(10, "a"))  # Ошибка: неверный тип данных!

-------------------------------------------------------------
5.0
Ошибка: деление на ноль!
Ошибка: неверный тип данных!
```

**Важные моменты:**

`return` внутри блока `try` позволяет вернуть результат или завершить выполнение функции, если всё прошло успешно.

Если возникает исключение, программа переходит в блок `except`, и `return` из него будет выполняться, если ошибка была обработана.

**Типы ошибок**

Чтобы понять, какую ошибку указывать в блоке `except`, необходимо знать, какие исключения (ошибки) могут возникать в коде. 
Python предоставляет множество типов ошибок (исключений), и для каждого типа ошибки нужно использовать соответствующий класс.

Некоторые распространённые исключения в Python:

`ZeroDivisionError` — возникает при попытке деления на ноль.

`ValueError` — возникает, когда функция получает аргумент неправильного типа, например, попытка преобразовать строку в число, но строка не является числом.

`TypeError` — возникает, когда операция выполняется с объектами неподходящих типов (например, сложение строки и числа).

`IndexError` — возникает, когда пытаются получить доступ к элементу списка по индексу, который выходит за пределы.

`KeyError` — возникает, когда пытаются обратиться к несуществующему ключу в словаре.

`FileNotFoundError` — возникает, когда файл, который пытаются открыть, не найден.

**Как узнать, какие ошибки могут возникать?**

Чтобы узнать, какое исключение может быть выброшено в процессе выполнения определённого кода, можно:

Прочитать документацию для функций и классов, которые вы используете, чтобы понять, какие ошибки могут быть выброшены.

Использовать `traceback` — это специальный модуль, который помогает узнать, какая ошибка была вызвана в процессе выполнения программы.

**Пример 3**

```
import traceback

try:
    x = 10 / 0
except Exception as e:
    print(f"Произошла ошибка: {e}")
    traceback.print_exc()  # Печатает полную информацию об ошибке

-----------------------------------------------
Произошла ошибка: division by zero
Traceback (most recent call last):
  File "<ipython-input-9-81c442dbf9d2>", line 4, in <cell line: 0>
    x = 10 / 0
        ~~~^~~
ZeroDivisionError: division by zero
```

# **try - except - finally**

Конструкция `try...except...finally` используется для обработки исключений с дополнительной гарантией выполнения кода в блоке `finally`, независимо от того, было ли исключение или нет. 
Это полезно, например, когда необходимо выполнить очистку ресурсов (закрыть файлы, закрыть соединения с базой данных и т. д.), даже если в блоке `try` произошло исключение.

```
try:
    # Код, который может вызвать исключение
    pass
except ExceptionType:
    # Код для обработки исключений, если возникло исключение
    pass
finally:
    # Код, который всегда выполняется, независимо от того, было ли исключение
    pass
```

**Пример 4**

```
def divide(a, b):
    try:
        result = a / b  # Попытка деления
        return result
    except ZeroDivisionError:
        return "Ошибка: деление на ноль!"  # Обработка исключения деления на ноль
    finally:
        print("Этот блок выполняется всегда.")  # Этот код всегда выполнится

# Пример вызова функции
print(divide(10, 2))  # Результат: 5.0, сообщение: Этот блок выполняется всегда.
print(divide(10, 0))  # Результат: Ошибка: деление на ноль!, сообщение: Этот блок выполняется всегда.

---------------------------------------------------------------
Этот блок выполняется всегда.
5.0
Этот блок выполняется всегда.
Ошибка: деление на ноль!
```
`return` в блоке `try` или `except` завершит выполнение функции, но `finally` выполнится даже после того, как функция вернёт значение.

Если в блоке `finally` есть код с `return`, он перекроет результат из `try` или `except`. Поэтому если в `finally` есть `return`, результат выполнения функции всегда будет зависеть от этого блока.

**Пример 5**

```
def example():
    try:
        return "Из try"
    except Exception:
        return "Из except"
    finally:
        return "Из finally"

print(example())  # Результат: "Из finally"

----------------------------------------------------
Из finally
```
