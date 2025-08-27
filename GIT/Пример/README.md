## Пример добавления изменений в уже существующий скрипт

Ниже пример как добавить изменения в уже существующий скрипт и отправить эти изменения из локального репозитория на удаленный.

*Если ветка была удалена, а необходимо продолжать работу над задачей, то можно снова создать ветку с таким же именем.*

В локальном репозитории были скрипты `.sql` с витриной.

<img width="646" height="133" alt="image" src="https://github.com/user-attachments/assets/2ca6464d-3291-49e7-b64e-60e043896289" />

В результате тестов пришлось поменять логику расчета в одном из файлов `3_udate.sql`.

**Порядок действий:**

Открываем GIT Bash в папке с локальным репозиторием.

<img width="920" height="444" alt="image" src="https://github.com/user-attachments/assets/bc43e5a4-1fb4-486e-a214-8fd3622763ab" />

Изначально откроется ветка OPALAB-14848, нам надо переключится на мастер, чтобы синхронизировать локальный репозиторий с удаленным. Вводим `git checkout master`

<img width="585" height="75" alt="image" src="https://github.com/user-attachments/assets/f448bdc6-ad55-451c-885e-1c684c917c7f" />

Делаем `git pull` - Скачивание изменений из удалённого репозитория в локальный

<img width="542" height="33" alt="image" src="https://github.com/user-attachments/assets/f6bcfde0-0e30-4608-b444-dbf63d8cd086" />

Далее переключаемся на нащу ветку `git checkout OPALAB-14848`

<img width="524" height="64" alt="image" src="https://github.com/user-attachments/assets/0951f3d3-2301-41be-ab08-396733ea42a4" />

Важно, чтобы название ветки было с номером задачи с которой работаем, в данном случае работаем с задачей `14848`.

*При работе с bitbucket от ветки `master` создаем новую локальную ветку с номером задачи. И всегда работаем только с локальной веткой*

<img width="571" height="22" alt="image" src="https://github.com/user-attachments/assets/a3bb1db2-fc9a-4899-ab12-d62b4cf8a42f" />

После каждого логически завершенного фрагмента работы добавляем изменения в свою локальную ветку (`add, commit`).
Добавляем изменения в скрипт `3_udate.sql` который лежит в локальном репозитории (удаляем старый код, добавляем новый).

Выполняем команду `git add .` (точка означает, что мы хотим добавить в git индекс все изменения): 

<img width="569" height="37" alt="image" src="https://github.com/user-attachments/assets/f042b3a7-a9fe-4f89-8d1e-bb98fc476fe3" />

Затем делаем `commit` и добавляем комментарий командой `git commit -m"Здесь пишем комментарий с изменениями":

<img width="582" height="67" alt="image" src="https://github.com/user-attachments/assets/a6fe8054-1344-4452-bd44-5ff7e439bb41" />

**Отправка изменений кода в BitBucket из GitBash**

После того как применили все изменения надо их отправить из локального репозитория на удаленный репозиторий.
Выполняем команду `git push`

<img width="612" height="189" alt="image" src="https://github.com/user-attachments/assets/b5462894-72f5-4e69-a0bd-b1ee281fd331" />

И проверяем статус локального репозитория, убеждаемся, что все изменения за день отправлены в bitbucket

<img width="623" height="135" alt="image" src="https://github.com/user-attachments/assets/70c64112-5910-40a9-8ad8-cb029ee7b4da" />

**Пройти код ревью**

Когда работа над задачей завершена и готова к код ревью, в репозитории BB создаем `pull request` на `merge` рабочей ветки с веткой `master` и наначаем `review` на сотрудника, ответсвенного за осуществление мерджа (или за проведение код ревью).

<img width="360" height="226" alt="image" src="https://github.com/user-attachments/assets/4b7e5b0b-84ee-46c1-b5e7-ec7a9f7aef9e" />

В качестве источника указываю свою рабочую ветку, в качестве назначениявыбираю `master`.

<img width="710" height="348" alt="image" src="https://github.com/user-attachments/assets/7d6f0e4f-cda0-40b5-94ae-b7bc29540009" />


Назначаю ревьювера моего кода:

<img width="541" height="286" alt="image" src="https://github.com/user-attachments/assets/d279153a-a89d-4a75-b589-7f665cff7a30" />

После проделанных шагов в BB. Надо написать письмо по шаблону, с просьбой провести код ревью и отправить на рег процессы.

<img width="1188" height="217" alt="image" src="https://github.com/user-attachments/assets/01e35346-632a-4a7b-84ca-8cd6d666f227" />



