# **Установка superset**

Создать папку, например superset на раб столе.

Открыть эту папку в cmd терминале.

Далее вводим команды в cmd.

Клонируем проект из github
`git clone https://github.com/apache/superset.git`
 
Переходим в директорию
`cd superset`

![image](https://github.com/user-attachments/assets/d931b628-bcb0-4731-b12e-8e542936ef1a)

Переключаемся на ветку релиза 2.1.0
`git checkout 2.1.0`
 
Проверяем статус (что переключились на правильный тег)
`git status`

Вводим команду чтобы открылся vscode `code .`

![image](https://github.com/user-attachments/assets/9fa38c3b-2d07-4c4c-bc5d-b8253353fb5f)

Открываем в vscode файл `docker-compose-non-dev.yml` меняем версию образа, который нужно использовать при развертывании. Делается это в 17 строке, вместо  `x-superset-image: &superset-image apache/superset:${TAG:-latest-dev}` пишем `x-superset-image: &superset-image apache/superset:2.1.0`

Открываем Docker Desctop

Запускаем установку (запустится скачивание образов с hub.docker.com). Вводим команду в cmd терминале `docker-compose -f docker-compose-non-dev.yml up`

По заверншении установки вводим в браузере `http://localhost:8088`

По умолчанию логин и пароль для входа: admin/admin.

Получаем superset

![image](https://github.com/user-attachments/assets/8fcab786-c7a9-4d72-a5b6-3b0d63619ec8)

Подключчаем развернутую в docker БД postgre к superset.

В HOST указываем host.docker.internal

Поскольку используем Superset в док-контейнере, не можем использовать ни 127.0.0.1, ни локальный хост, поскольку они разрешаются в контейнер, а не в хост.

![image](https://github.com/user-attachments/assets/2c6fa41d-b8a6-46ad-94b3-2bca7ca35cf8)

Если сделать запрос, видим что подключились к тестовой БД

![image](https://github.com/user-attachments/assets/8242190c-1fe7-419b-8b89-601019bce022)
