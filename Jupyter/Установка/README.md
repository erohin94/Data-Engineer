**Jupyter**

1.Создадим файл docker-compose.yml. С необходимыми настройками.

```
version: '3'

services:
  jupyter:
    image: jupyter/base-notebook
    container_name: jupyter
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    restart: always
```

```
docker-compose up -d
```

![image](https://github.com/user-attachments/assets/9442b3d0-d0d4-4d94-8bc0-dc73217b387d)

Заходим по ссылке http://localhost:8888/

Появится следующее окно:

![image](https://github.com/user-attachments/assets/d403d881-660c-4e4e-a810-b3aa710a3813)

Вводим в терминале 

`docker logs jupyter`

![image](https://github.com/user-attachments/assets/d87b2f83-ea6a-402a-9baf-7139a744595f)

![image](https://github.com/user-attachments/assets/ce8e033f-56a1-4742-92ed-09b970ec4291)

И ищем строку вида `http://127.0.0.1:8888/lab?token=cc9b05f96f`, копируем всю строку и вставляем в браузер, после чего открывается ноутбук.

Либо копируем токен и вставляем в поле `Password or token` и так же переходим в ноутбук.

![image](https://github.com/user-attachments/assets/84140b14-f9e2-4c97-ae52-e9c4cefb27c7)

Так же можно сделать запуск без ввода логина или токена. Создав `.yml` файл, добавив в него строку `command: start-notebook.sh --NotebookApp.token=''` следующего вида

```
services:
  jupyter:
    image: jupyter/base-notebook
    container_name: jupyter
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    restart: always
    command: start-notebook.sh --NotebookApp.token=''
```
