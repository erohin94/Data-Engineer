# Компоненты Airflow

# **Основные компоненты пользовательского интерфейса**

В адресной строке браузере ввеcти http://127.0.0.1:8080.

![image](https://github.com/user-attachments/assets/8de383d3-e46a-4a6b-bfe9-260711923061)

Пользователь airflow/пароль airflow.

![image](https://github.com/user-attachments/assets/f0cbdb49-04e0-44a4-bc77-9e828d818922)

Красной рамкой выделено сообщение от Airflow, что ещё не запущен Планировщик.

```The scheduler does not appear to be running. The DAGs list may not update, and new tasks will not be scheduled.```

На главном экране синей рамкой выделен список примеров, которые Airflow грузит в панель по умолчанию. Чтобы отключить их загрузку необходимо в yaml файле поменять параметр на false (62 строка):

```AIRFLOW__CORE__LOAD_EXAMPLES: 'false'```

Сразу после входа в панель Airflow виден список всех DAG, которые подгрузил Airflow:

![image](https://github.com/user-attachments/assets/cec4c2e7-89d4-4c76-a37c-67cdeb4cd3ce)

**Pause/Unpause DAG** — слева находится переключатель для включения/выключения DAG. По умолчанию все новые DAG будут остановлены. Чтобы запустить DAG его необходимо предварительно включить.

**Колонка Owner** обозначает владельца/автора DAG. Эта опция задаётся в коде.

**Runs** — показывает состояние запусков прошлых DAG. Есть 3 состояния:

1.Успешно выполнен

2.Выполняется

3.Есть ошибки при выполнении

**Schedule** — показывает с какой периодичностью будет запускаться DAG. Если значение None, то запуска по расписанию не будет, но можно запускать вручную, например.

**Last Run** — дата и время последнего запуска DAG

**Recent Tasks** — отражает текущее состояние последних запусков DAG (по факту последний запуск DAG и его операторов)

**Actions** — кнопки манипуляции с DAG. Можно запустить DAG вручную, обновить или удалить DAG.

**Links** — список для быстрого доступа к просмотру кода DAG, деталей выполнения, просмотру в виде графа или диаграммы Ганта, анализ времени выполнения задач и т.д.

## **Просмотр DAG**

Если кликнуть на любой DAG из списка, то видно детальную информацию по нему.

![image](https://github.com/user-attachments/assets/8e2d776d-2fe8-4cea-bdaf-75e08976077c)

**Details** — детальная информация по DAG, включая названия операторов, автора, начальное время старта DAG и т.д.

**Graph** — просмотр DAG и зависимостей между операторами в виде графа, также слева находится статус выполнения всех операторов, входящих в DAG с легендой. На статусы можно кликать, чтобы посмотреть более детальную информацию.

**Gantt** — отображает историю выполнения DAG в виде Диаграммы Ганта. Очень удобно, когда в DAG входит множество операторов, которые могут выполняться параллельно.

**Code** — просмотр кода DAG.

**Audit Log** - на вкладке « Журналы аудита» отображается список событий, произошедших в среде Airflow и относящихся к выбранному DAG, запуску DAG или экземпляру задачи.

**Run Duration** — «Продолжительность выполнения» отображается столбчатая диаграмма продолжительности каждого выполнения DAG с течением времени.


## **Панель администратора Airflow**

![image](https://github.com/user-attachments/assets/9c842b97-76fa-4155-af19-78f61e47e05e)


**Variables**

В этом разделе можно управлять переменными, которые будут храниться в базе данных Airflow. Удобно для хранения различной информации, например, адреса хостов удалённых сервисов. Нежелательно в этом разделе хранить данные доступов, т.к. переменные хранятся в открытом виде и могут быть скомпрометированы третьими лицами.

**Configurations**

Раздел позволяет редактировать настройки Airflow, используя графический интерфейс. По умолчанию опция отключена из соображений безопасности.

**Connections**
Раздел для хранения данных о доступе к различным сервисам: базам данных, облачным провайдерам, сторонним API сервисам и т.д. Не рекомендуется в DAG коде хранить пароли и секретные ключи, а использовать для этого раздел Connections, например.

При использовании Connections в коде необходимо лишь будет передать значение conn_id. На практике увидим как это удобно и просто.

**Plugins**

Раздел для управления плагинами Airflow. По умолчанию плагины можно подгрузить, разместив код по пути AIRFLOW_HOME/plugins.

**Pools**

Возможность задать пул или другими словами некое ограничение на количество параллельно выполняющихся задач. Представим, что вы хотите регулярно качать данные с внешнего сервиса. У сервиса есть ограничение на количество одновременных соединений — 2. В этом случае вы создаёте пул со значением 2 и присваиваете ему имя. Далее во всех операторах, отвечающих за скачивание данных, передаёте название этого пула.

**XComs**

Это механизм обмена сообщениями между операторами. Т.к. задачи могут выполняться на разных компьютерах, то получить возвращаемое значение одного оператора и передать другому привычным способом не получится (например, путём цепочек вызовов или присвоением значения переменной). Для таких ситуаций и создан XCom (cross-communication). Механизм работает через базу данных. По сути это аналог key-value базы, один оператор записывает значение под определённым ключом, а другой оператор может получить это значением, используя этот ключ. Не рекомендуется таким способом передавать большие сообщения, т.к. это требует дополнительных накладных расходов.

В этом разделе можно увидеть все существующие сообщения, созданные операторами.

## **БД**

База данных это сердце всего Apache Airflow. В ней хранятся записи об успешных и неуспешных запусках пайплайнов, конфигурационные настройки, информация о пользователях и так далее. Разработчики Airflow называют её metadata database.

Сообщество рекомендует в продакшене использовать PostgreSQL.

## DAG

![image](https://github.com/user-attachments/assets/f6a8a88a-2832-4e44-b280-53ee703254fe)

На картинке выше представлен пример DAG, где Task A это начало выполнения, а Task E это финиш. Выполнение задач происходит слева направо. Зависимость между задачами показана стрелкой. Например, Task B и Task C зависят от Task A, а Task E зависит от всех задач, находящихся слева от него.

Задачи, входящие в состав DAG, в Apache Airflow называются операторами(Operator).


Сcылки:

https://www.astronomer.io/docs/learn/airflow-ui/