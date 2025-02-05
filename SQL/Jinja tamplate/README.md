# Применение jinja для фильтрации показателей

**Создаем датасет для фильтра**

Сгенерируем серию с '2025-01-01' по '2025-03-02' и далее сгрупирую по номеру месяца

```
SELECT month_number, 
       CONCAT(TO_CHAR(MIN(day), 'DD.MM.YYYY'), ' - ', TO_CHAR(MAX(day), 'DD.MM.YYYY')) as "Период", 
       CONCAT(TO_CHAR(MIN(day), 'YYYY-MM-DD'), ' - ', TO_CHAR(MAX(day), 'YYYY-MM-DD')) as "Период jinja" 
FROM(
   SELECT day, EXTRACT(month FROM day) AS month_number
   FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day   
      
    ) as rez
group by 1
order by 1
```

![image](https://github.com/user-attachments/assets/72f772d0-4685-4dcd-a4f4-d0424e3a30d7)

**Создаем датасет для показателя**

Также сгенерируем датасет для показателя, получим таблицу с датами и номером дня конкретного месяца

```
SELECT day, EXTRACT(day FROM day) AS day_number
FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day
```

![image](https://github.com/user-attachments/assets/91a43a21-7b1e-4fe7-8c24-1ba88db372cb)



