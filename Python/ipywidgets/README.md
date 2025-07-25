# **ipywidgets**

`ipywidgets` — это библиотека для создания интерактивных элементов управления (виджетов) в Jupyter Notebook и JupyterLab. Она позволяет связывать Python-код с пользовательским интерфейсом: ползунками, выпадающими списками, кнопками и другими элементами.

**Список часто используемых виджетов:**

| Виджет         | Назначение                                   |
| -------------- | -------------------------------------------- |
| `IntSlider`    | Ползунок для целых чисел                     |
| `FloatSlider`  | Ползунок для дробных чисел                   |
| `Dropdown`     | Выпадающий список                            |
| `Text`         | Однострочное текстовое поле                  |
| `Textarea`     | Многострочное текстовое поле                 |
| `Checkbox`     | Флажок (да/нет)                              |
| `ToggleButton` | Кнопка-переключатель                         |
| `Button`       | Кнопка действия                              |
| `RadioButtons` | Группа переключателей                        |
| `Output`       | Блок вывода                                  |
| `HBox`, `VBox` | Компоновка виджетов по горизонтали/вертикали |

----------------------------------------------------------------------------------------

**widgets.Dropdown**

Dropdown (выпадающий список) — это интерактивный элемент управления (виджет) в Jupyter Notebook, 
который позволяет пользователю выбирать значение из предопределённого списка.

```
widgets.Dropdown(
    options,        # список значений или словарь {подпись: значение}
    value,          # значение по умолчанию
    description,    # текст слева от выпадающего списка
    disabled,       # если True — нельзя выбрать (серый)
    layout,         # макет (например, ширина/высота)
    style           # стиль (например, {'description_width': 'initial'})
)
```

----------------------------------------------------------------------------------------

**dropdown.observe**

`dropdown.observe(...)` — наблюдение за изменениями

В `ipywidgets` у каждого виджета есть метод `.observe()` — он позволяет реагировать на изменение свойства виджета, например, когда пользователь выбирает другой элемент из Dropdown.

Пример

```
import ipywidgets as widgets
from IPython.display import display

dropdown = widgets.Dropdown(
    options=['Кошка', 'Собака', 'Попугай'],
    value='Кошка',
    description='Питомец:',
)

def on_change(change):
    print(change)

dropdown.observe(on_change)
display(dropdown)

-------------------------------
Питомец: Собака
{'name': '_property_lock', 'old': traitlets.Undefined, 'new': {'index': 1}, 'owner': Dropdown(description='Питомец:', options=('Кошка', 'Собака', 'Попугай'), value='Кошка'), 'type': 'change'}
{'name': 'label', 'old': 'Кошка', 'new': 'Собака', 'owner': Dropdown(description='Питомец:', index=1, options=('Кошка', 'Собака', 'Попугай'), value='Кошка'), 'type': 'change'}
{'name': 'value', 'old': 'Кошка', 'new': 'Собака', 'owner': Dropdown(description='Питомец:', index=1, options=('Кошка', 'Собака', 'Попугай'), value='Собака'), 'type': 'change'}
{'name': 'index', 'old': 0, 'new': 1, 'owner': Dropdown(description='Питомец:', index=1, options=('Кошка', 'Собака', 'Попугай'), value='Собака'), 'type': 'change'}
{'name': '_property_lock', 'old': {'index': 1}, 'new': {}, 'owner': Dropdown(description='Питомец:', index=1, options=('Кошка', 'Собака', 'Попугай'), value='Собака'), 'type': 'change'}
```

Что такое `change`?

`change` — это словарь с описанием того, что изменилось. Вот как он может выглядеть:

```
{
 'name': 'value', # Имя свойства, которое изменилось (например, 'value')
 'old': 'Кошка', # Старое значение
 'new': 'Собака', # Новое значение (что выбрал пользователь)
 'owner': Dropdown(...), # Сам виджет (dropdown, slider, и т.д.)
 'type': 'change' # 	Тип события. Всегда 'change' для обычного изменения
}
```

----------------------------------------------------------------------------------------

**button.on_click**

`button.on_click(...)` — реакция на нажатие кнопки

----------------------------------------------------------------------------------------

**widgets.Button**

Это кнопка, которую можно нажать в интерфейсе Jupyter Notebook, чтобы запустить Python-функцию.

```
widgets.Button(
    description='Текст кнопки',
    disabled=False,                   # если True — кнопка "засерая", недоступна
    button_style='',                  # 'primary', 'success', 'info', 'warning', 'danger' или ''
    tooltip='Подсказка при наведении',
    icon='check'                      # Иконка из FontAwesome, например: 'check', 'refresh', 'upload'
)
```

----------------------------------------------------------------------------------------

**widgets.Output**

`widgets.Output` — Позволяет выводить информацию (текст, графику, ошибки) в ограниченную область, а не прямо в ячейку.

Что делает `widgets.Output`?

`Output` позволяет:

- выводить `print()`, `display()`, графики `(matplotlib, plotly)` внутри себя;

- изолировать вывод (удобно в интерфейсах с кнопками и интерактивными элементами);

- очищать и обновлять содержимое при необходимости.
















