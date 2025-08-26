## Пример добавления изменений в уже существующий скрипт

В локальном репозитории были скрипты `.sql` с витриной.

<img width="646" height="133" alt="image" src="https://github.com/user-attachments/assets/2ca6464d-3291-49e7-b64e-60e043896289" />

В результате тестов пришлось поменять логику расчета в одном из файлов `3_udate.sql`.

**Порядок действий:**

Открываем GIT Bash в папке с локальным репозиторием.

<img width="920" height="444" alt="image" src="https://github.com/user-attachments/assets/bc43e5a4-1fb4-486e-a214-8fd3622763ab" />

Важно, чтобы название ветки было с номером задачи с которой работаем, в данном случае работаем с задачей `14848`.

*При работе с bitbucket от ветки `master` создаем новую локальную ветку с номером задачи. И всегда работаем только с локальной веткой*

<img width="571" height="22" alt="image" src="https://github.com/user-attachments/assets/a3bb1db2-fc9a-4899-ab12-d62b4cf8a42f" />

Выполнем команду `git pull` - Скачивание изменений из удалённого репозитория в локальный

<img width="571" height="35" alt="image" src="https://github.com/user-attachments/assets/42fbeb35-d1eb-4e4f-b4f5-565cbd4e572f" />

После каждого логически завершенного фрагмента работы добавляем изменения в свою локальную ветку (`add, commit`).
Добавляем изменения в скрипт `3_udate.sql` который лежит в локальном репозитории (удаляем старый код, добавляем новый).

Выполняем команду `git add .` (точка означает, что мы хотим добавить в git индекс все изменения): 

<img width="569" height="37" alt="image" src="https://github.com/user-attachments/assets/f042b3a7-a9fe-4f89-8d1e-bb98fc476fe3" />

После добавления изменений в индекс, проверяем статус снова: `git status`. Git должен показать, что изменения добавлены в индекс и готовы для коммита.

<img width="563" height="115" alt="image" src="https://github.com/user-attachments/assets/6aeff96e-a34f-4126-8acd-09930bfeb3ae" />

Затем делаем `commit` и добавляем комментарий командой `git commit -m"Здесь пишем комментарий с изменениями":

<img width="582" height="67" alt="image" src="https://github.com/user-attachments/assets/a6fe8054-1344-4452-bd44-5ff7e439bb41" />

**Отправка изменений кода в BitBucket из GitBash**

После того как применили все изменения надо их отправить на удаленный репозиторий.
Выполняем команду `git push`

<img width="612" height="189" alt="image" src="https://github.com/user-attachments/assets/b5462894-72f5-4e69-a0bd-b1ee281fd331" />

И снова проверяем статус локального репозитория, убеждаемся, что все изменения за день отправлены в bitbucket

<img width="623" height="135" alt="image" src="https://github.com/user-attachments/assets/70c64112-5910-40a9-8ad8-cb029ee7b4da" />
