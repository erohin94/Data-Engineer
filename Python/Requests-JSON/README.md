# **📦 Requests + JSON Cheatsheet**

**🛰️ Отправка запросов и базовые методы**

| Цель                          | Код / Метод                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 📡 Отправка GET-запроса      | `response = requests.get(url, params=params)`                              |
| 📤 Отправка POST-запроса     | `response = requests.post(url, json=data)`                                 |
| ✅ Проверка успешного ответа | `response.ok` или `response.status_code == 200`                            |
| 📥 Получить JSON из ответа   | `data = response.json()` (только если ответ — JSON)                        |
| 📄 Получить текст ответа     | `response.text`                                                            |
| 📦 Получить байты (файл)     | `response.content`                                                         |
| 🌐 Получить URL              | `response.url`                                                             |
| 🧾 Заголовки ответа          | `response.headers`                                                         |
| 💣 Ошибки HTTP               | `response.raise_for_status()` — выбросит исключение, если статус ≥ 400    |

**🧾 Работа с JSON (модуль json)**

| Цель                          | Код                                                                          |
|------------------------------|-------------------------------------------------------------------------------|
| 📤 Python → JSON строка      | `json_str = json.dumps(data, ensure_ascii=False, indent=2)`                 |
| 📥 JSON строка → Python dict | `data = json.loads(json_str)`                                               |
| 💽 Сохранить в файл          | `json.dump(data, f, ensure_ascii=False, indent=2)`                          |
| 📂 Загрузить из файла        | `data = json.load(f)`                                                       |

**🧰 Полезные методы словаря (dict) в JSON**

| Метод               | Назначение                                   |
|---------------------|----------------------------------------------|
| `data.get("key")`   | Безопасно получить значение (или None)       |
| `data["key"]`       | Получить значение (ошибка, если ключа нет)   |
| `data.items()`      | Пары ключ–значение                           |
| `data.keys()`       | Все ключи                                    |
| `data.values()`     | Все значения                                 |
