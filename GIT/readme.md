# Подключение к Github

**Github** - это обычный сайт, куда можно загрузить cвой код или скачать его оттуда. 

**Репозиторий** - в простонародье это просто папка.

Сначала подключимся к Github чтобы постоянно не вводить логин и пароль. Для этого нам нужно создать ключ (ссылку), который свяжет наш компьютер с Github. 

Заходим в terminal или командную строку. Пишем:

```ssh-keygen```

Нажимаем везде Enter. В Overwrite (y/n)? нажать y, так как у меня уже был ключ, поэтому чтобы пересоздать нажимаем y.

```C:\Users\erohi>ssh-keygen
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\erohi/.ssh/id_ed25519):
C:\Users\erohi/.ssh/id_ed25519 already exists.
Overwrite (y/n)? y
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\erohi/.ssh/id_ed25519
Your public key has been saved in C:\Users\erohi/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:PjS/4ivgfjMW/PMYkzvafhjjhxOoAU3FWjhhjleAvzftktczcTKMTIERFN9805 erohi@LAPTOP-4CD5HV7A
The key's randomart image is:
   +--[ED25519 256]--+
|   ...ooooo           |
|    .+ .              |
|  . o  o . .          |
|   o . ofd = . E      |
|    o  .Sdf+ . .      |
|   o+. =.+o o .       |
|  .. == Bdfd .oooo . .|
|    ..+=.= .. +       |
|     oo=Bodoof.  . oo |
   +----[SHA256]-----+
```

Дальше нам нужно открыть файл, где создался этот ключ (просто шифр из многобукв). Username у вас свой!

Переходим в папку с ключом: ```cd .ssh```

Проверяем содержимое папки: ```dir```. Находим публичный ключ, копируем его название и открываем.

```type id_ed28871.pub```

Копируем ключ:

```ssh-ed28871 AAAAC3ЬzaC1lZDI1NTslvlsfvdvl9951891vfvskns.s+z5HFG erohi@LAPTOP-4CD9HV6A```

Заходим в настройки SSH and GPG keys. Нажимаем New SSH key.

![image](https://github.com/user-attachments/assets/d3c38a86-ca74-44c4-827f-7afa85b1d855)

Вставляем скопированный ключ.

![image](https://github.com/user-attachments/assets/5281c965-a78d-410c-8b09-3d61a4afbcce)

Теперь можно скачивать и загружать на git

![sds](https://github.com/user-attachments/assets/1ddce372-0d53-41ee-9226-db0444354c7f)

# Команды GIT

Чтобы добавить файлы или папки в репозиторий на GitHub, выполнить следующие шаги:

**1. Клонировать репозиторий на локальную машину (к себе на компьютер):**

```git clone https://github.com/пользователь/репозиторий.git``` - Git может запросить пароль, если вы используете HTTPS для доступа к репозиторию.

```git clone git@github.com:erohin94/Data-Engineer.git``` - Поэтому используем SSH соединение.

Заменить пользователь/репозиторий на ваш актуальный путь.

![image](https://github.com/user-attachments/assets/5bfa56c3-ba00-42f9-a3d3-a5fcd02e8b2d)

![image](https://github.com/user-attachments/assets/ade1192a-d195-4600-942b-520700f3447b)

**2. Перейти в папку репозитория:**

После того как репозиторий клонирован, открыть терминал (или командную строку) и перейти в папку с репозиторием:

```cd репозиторий```

![image](https://github.com/user-attachments/assets/aac92759-8950-4d38-96fe-c9b3b4150093)


**3. Создайте или переместите папку:**

Если уже есть папка, то чтобы переместить эту папку в локальный репозиторий

```move C:\Users\erohi\Desktop\airflow_project C:\Users\erohi\Desktop\Github\Data-Engineer\Airflow```

**4. Проверить статус**

```git status```

![image](https://github.com/user-attachments/assets/061c8c4a-ad59-4dfc-8696-305d504c6fe7)

Git сообщает, что папка airflow_project/ ещё не отслеживается (это неотслеживаемый файл), и нужно добавить её в индекс Git, чтобы зафиксировать изменения.

**4. Добавить изменения в Git:**

Теперь надо добавить файлы или папки в индекс Git, чтобы они были готовы к коммиту:

```git add airflow_project/```

Это добавит перемещённую папку airflow_project/ в Git и начнет отслеживать её.

Если хотим добавить все изменения в репозитории (включая другие файлы и папки, если таковые имеются), использовать команду:

```git add .```

**5. После добавления изменений в индекс, проверьте статус снова:**

```git status```

Git должен показать, что изменения добавлены в индекс и готовы для коммита.

**6. Закомитьте изменения:**

Теперь надо сделать коммит, чтобы зафиксировать изменения:

```git commit -m "Перемещена папка airflow_project в репозиторий"```

7. Отправьте изменения на GitHub:
После коммита отправьте изменения в репозиторий на GitHub:

`git push origin main`
Если ваша ветка называется не main, замените её на актуальное название ветки.

Теперь ваша папка и файлы должны быть добавлены в репозиторий на GitHub.
