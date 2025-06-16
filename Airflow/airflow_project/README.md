# Airflow проект

[Инструкция по установке Airflow](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/README.md)


**TaskFlow API**

В Apache Airflow 2.0 появился новый способ описания DAG и PythonOperator — TaskFlow API. TaskFlow API это синтаксический сахар, который делает код чище и проще для чтения. Во второй версии Apache Airflow были введены 2 декоратора: dag и task.

Давайте посмотрим как выглядит предыдущий код, переписанный на TaskFlow API: [DAG](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/airflow_project/dags/taskflow_dag_with_two_operators.py)

Когда вы добавляете новый DAG в папку с DAG'ами в Apache Airflow,нужно перезапустить планировщик (scheduler), чтобы новый DAG был загружен и появился в веб-интерфейсе.

Перезапустите контейнер с планировщиком: ```docker restart airflow_project-airflow-scheduler-1```

![image](https://github.com/user-attachments/assets/4e5d1120-f7f9-49ab-aa7c-b7ecdecdab09)

Чтобы сформировать объект DAG, необходимо обернуть функцию декоратором dag. Этот декоратор принимает те же аргументы. Чтобы превратить функцию в PythonOperator, её необходимо обернуть в декоратор task.

Обратите внимание, что инстанс DAG должен быть доступен в глобальном пространстве при импорте кода планировщиком. Именно поэтому я вызываю функцию, обернутую в декоратор dag и присваиваю переменной main_dag. Если этого не сделать, то планировщик не сможет найти DAG.

Заметьте, что явно не указываем task_id, он берётся из названия оборачиваемой функции.

Далее во всех примерах, где будет нужен PythonOperator я буду использовать TaskFlow API. Мы также рассмотрим как TaskFlow API позволяет "бесшовно" передавать возвращаемые значения из одного оператора в другой. До TaskFlow API необходимо было явно использовать XCom.

Подробный пост на тему TaskFlow API [TaskFlow API в Apache Airflow 2.0](https://startdatajourney.com/ru/course/apache-airflow-2/modules/11/36/1#:~:text=TaskFlow%20API%20%D0%B2%20Apache%20Airflow%202.0)
