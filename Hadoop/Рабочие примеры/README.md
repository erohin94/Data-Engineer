# **Примеры SQL запросов**

**Удалить таблицу**

```
DROP TABLE IF EXISTS schema_name.ees_table_name
```

**Создание таблиц без дублей для VIEW**

```
DROP TABLE IF EXISTS schema_name.ees_table_name

CREATE TABLE IF NOT EXISTS schema_name.ees_table_name (
                                        resume_id string,
                                        owner_id int,
                                        url string,
                                        url_w_contacts string,
                                        vacancy_code int,
                                        search_status string,
                                        area_id int,
                                        t_changed_dttm timestamp
                                        ) 
                                        stored as parquet
                                        
INSERT INTO schema_name.ees_table_name
SELECT resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, area_id, t_changed_dttm
FROM (SELECT *, 
	  ROW_NUMBER() OVER(PARTITION BY resume_id ORDER BY resume_id) as rn 
	  FROM schema_name.ees_table_name_tmp) ees_search_result
WHERE rn = 1 

SELECT count(*) FROM schema_name.ees_table_name
```

**Создание VIEW для ML модели на основе таблиц без дублей**

```
DROP VIEW IF EXISTS schema_name.ees_model_input

CREATE VIEW IF NOT EXISTS schema_name.ees_model_input AS
with vacancy as (
				 SELECT priority AS vacancy_cd, 
				        priority_desc AS direction_cd
				 FROM dm_schema.view_model_table
				 WHERE TO_DATE(active_date_to) > CURRENT_DATE() and CAST(resume_search_target_daily AS int) > 0 
				 group by 1, 2
				 )
select sr.vacancy_code, v.direction_cd, sr.search_status, sr.url_w_contacts,  ar.*
from schema_name.ees_table_name sr
join schema_name.ees_table_application_resume ar
    on sr.resume_id = ar.id
    and cast(sr.t_changed_dttm as date) = cast(ar.t_changed_dttm as date)
left join vacancy v
    on sr.vacancy_code = cast(v.vacancy_cd as int)
where 1=1
--and cast(sr.t_changed_dttm as date) = cast(now() as date) --Раскоментировать
and ((sr.vacancy_code = 1004 and ar.area_id in ('1')) or 
(sr.vacancy_code = 1008 and ar.area_id in ('3', '70', '99', '107')) or 
(sr.vacancy_code = 1009 and ar.area_id in ('3', '99', '107')) or 
(sr.vacancy_code = 1011 and ar.area_id in ('99')) or 
(sr.vacancy_code = 10012 and ar.area_id in ('24', '3', '88', '53', '1', '66', '4', '68', '76', '78', '2', '90', '99')))
```

**Удалить строки которые позже определенной даты, не работает для таблиц созданных в формате PARQUET**

```
DELETE FROM schema_name.ees_hh_resume WHERE cast(t_changed_dttm as timestamp) > cast('2025-05-16 11:56:00' as timestamp) 
```

**Создание временных таблиц на основе SQL запроса**

```
---------------------------------------------------------------------------------
CREATE TABLE schema_name.ees_hh_application_resume_erohin_tmp STORED AS PARQUET AS --Создаем временную таблицу
SELECT *
FROM schema_name.ees_hh_application_resume_erohin  
WHERE cast(t_changed_dttm as timestamp) < cast('2025-05-16 11:56:00' as timestamp) 

DROP TABLE IF EXISTS schema_name.ees_hh_application_resume_erohin --Дропаем основную таблицу

ALTER TABLE schema_name.ees_hh_application_resume_erohin_tmp RENAME TO schema_name.ees_hh_application_resume_erohin --Переименовываем временную таблицу в основную

SELECT count(*) FROM schema_name.ees_hh_application_resume_erohin --Проверка
---------------------------------------------------------------------------------
```



**Тесты**

```
--------------------------------------------------------------------------------- 
SELECT resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, area_id, t_changed_dttm
FROM (SELECT *, 
	  ROW_NUMBER() OVER(PARTITION BY resume_id ORDER BY resume_id) as rn 
	  FROM schema_name.ees_table_name_tmp) ees_search_result
WHERE rn = 1 
---------------------------------------------------------------------------------        
  
   
   
   
---------------------------------------------------------------------------------
--Проверка VIEW
SELECT Count(*)
FROM schema_name.ees_model_input  
      
SELECT *
FROM schema_name.ees_model_input   
---------------------------------------------------------------------------------      
     
          


--------------------------------------------------------------------------------- 
SELECT *
FROM dm_table.view_model
WHERE TO_DATE(active_date_to) > CURRENT_DATE() and CAST(resume_search_target_daily AS int) > 0 



WITH handbook_es as (
			SELECT *,  
			ROW_NUMBER() OVER(PARTITION BY priority, priority_desc, region ORDER BY active_date_from DESC, resume_search_target_daily DESC) AS rn
			FROM dm_es.view_model
WHERE TO_DATE(active_date_to) > CURRENT_DATE() and CAST(resume_search_target_daily AS int) > 0 AND CAST(priority as int) IS NOT NULL
)
SELECT active_date_from, active_date_to, priority, priority_desc, region, resume_search_target_daily, salary_value, hdp_datetime 
FROM handbook_es
WHERE rn = 1



SELECT * 
FROM dm_es.view_model
WHERE cast(priority as int) is not null

SELECT cast('sfaf' as int), cast('12323' as int)


SELECT priority, priority_desc, region, COUNT(*) as count_vacancy
FROM dm_es.view_model
WHERE TO_DATE(active_date_to) > CURRENT_DATE() and CAST(resume_search_target_daily AS int) > 0
GROUP BY priority, priority_desc, region 
--HAVING COUNT(*) > 1 
---------------------------------------------------------------------------------      
 



---------------------------------------------------------------------------------
SELECT id, name 
FROM schema_name.ees_xref_hh_areas 
WHERE syslib.utf8_lower(name) IN ('волгоград', 'екатеринбург', 'казань', 
									'краснодар', 'москва', 'нижний новгород', 'новосибирск', 'омск', 
										'оренбург', 'ростов-на-дону', 'самара', 
											'санкт-петербург', 'томск', 'уфа', 'чебоксары')

--WHERE LOWER(name) in ('Москва', 'Астрахань')

SELECT LOWER('QWERTY') --> Результат qwerty 
SELECT syslib.utf8_lower('МОСКВА') --> Результат МОСКВА 
---------------------------------------------------------------------------------      
```

```
-- Проверка интервалов времени

SELECT LAST_DAY(DATE_SUB(TRUNC(NOW(), 'mm'), 1)) --Возвращает последний день месяца для указанной даты

SELECT DATE_SUB(TRUNC(DATE_ADD(TRUNC(NOW(), 'mm'), INTERVAL 0 MONTH), 'mm'), 150)

SELECT TRUNC(NOW(), 'dd') --Округление до дня

SELECT DATE_ADD(TRUNC(NOW(), 'dd'), INTERVAL 0 MONTH) -- Добавляет интервал 0 месяцев к сегодня

SELECT TRUNC(DATE_ADD(TRUNC(NOW(), 'dd'), INTERVAL 0 MONTH), 'mm') --Округление до дня, добавление интервала 0 месяцев, округления до начала месяца
