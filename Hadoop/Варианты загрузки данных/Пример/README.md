## Пример инкрементальной загрузки данных

Есть витрина `sbxm_hr.ees_client_flow_to_office_test`

```
DROP TABLE IF EXISTS sbxm_hr.ees_client_flow_to_office_test
/
CREATE TABLE IF NOT EXISTS sbxm_hr.ees_client_flow_to_office_test (
							--user_login STRING COMMENT 'Логин сотрудника',
							auto_card_id INT COMMENT 'ИД сотрудника в исторической витрине',
							deviation_month_avg_rt DECIMAL(28,6) COMMENT 'Cреднее отклонение фактического времени обслуживания и нормативного времени обслуживания за месяц  для сотрудника',
							waiting_time_month_avg_nval DECIMAL(28,6) COMMENT 'Среднее время ожидания приема за месяц',
							popular_operation STRING COMMENT 'Наиболее частый тип обращения за месяц',
							unique_operation_cnt INT COMMENT 'Количество уникальных видов обращений за месяц',
							non_vip_rt DECIMAL(28,6) COMMENT 'Доля не ВИП-клиентов за месяц',
							vip_rt DECIMAL(28,6) COMMENT 'Доля ВИП-клиентов за месяц',
							activity_per_office_rt DECIMAL(28,6) COMMENT 'Нагрузка сотрудника в ДО',
							operation_avg_cnt DECIMAL(28,6) COMMENT 'Средний клиентопоток на сотрудника',
							customer_flow_compl_rt DECIMAL(28,6) COMMENT 'Флаг выполнения критерия Клиентопотока',
							operation_avg_time_sec_nval DECIMAL(28,6) COMMENT 'Среднее время выполнения операций',
							operation_avg_time_flg TINYINT COMMENT 'Флаг выполнения критерия (Среднее время выполнения операций)',
							sell_operation_rt DECIMAL(28,6) COMMENT 'Доля операций с продажами в структуре клиентопотока у сотрудника',
							sell_operation_flg TINYINT COMMENT 'Флаг выполнения критерия (Доля операций с продажами)',
							service_operation_rt DECIMAL(28,6) COMMENT 'Доля сервисных операций в структуре клиентопотока',
							service_operation_flg TINYINT COMMENT 'Флаг выполнения критерия (Доля сервисных операций)',
							report_dt TIMESTAMP COMMENT 'Отчетная дата',
							t_changed_dttm TIMESTAMP COMMENT 'Дата и время обновления витрины')
PARTITIONED BY (report_year INT COMMENT 'Год события')							
COMMENT 'Витрина данных по посещениям ДО'
STORED AS PARQUET
```
**Требования к витрине**

**Первичный расчет витрины:** с 2020-01-01

**Дальнейший расчет витрины:** производится ежемесячно

**Обновление данных:** инкрементально

**Регламентное время готовности данных:** в 11-00 третьего числа каждого месяца

Надо реализовать инкрементальную загрузку данных. Считаем что витрина обновляется четко в начале мясяца, за предыдущий месяц.
Данные в источник попадают без задержки. Возможно несколько вариантов. 

**Первый**, если витрина пустая, то загружаем все данные из источника.

**Второй**, если в витрине есть данные, то загружаем тот месяц, которого нет. 

Например, загрузка происходит в третьих числах каждого месяца.

Представим что находимся в 03.08.2025. В витрине данные только за июнь, за июль данных нет. Тогда надо будет загрузить данные за весь отчетный месяц - за июль. 
При этом данные за первые числа августа в витрину попасть не должны.

**Третий**, если в витрине нет данных за два последних месяца, например последняя загрузка только за май, данных за июнь, июль нет. Соответственно 03.08.2025 будем загружать данные за июнь и июль.
С 01.06.2025 по 31.07.2025.



Ниже пример получения первичной выборки на основе источника. На этой первичной выборке рассчитываются остальные атрибуты и собирается витрина. Но инкремент реализован именно на ней.

Создаем таблицу `sbxm_hr.ees_first_sample_non_norm_time_tmp_test` -первичная выборка.
```
DROP TABLE IF EXISTS sbxm_hr.ees_first_sample_non_norm_time_tmp_test
/
CREATE TABLE IF NOT EXISTS sbxm_hr.ees_first_sample_non_norm_time_tmp_test (
										party_global_rk DECIMAL(18,0) COMMENT 'Клиент',
										user_login STRING COMMENT 'Логин сотрудника',
										event_rk DECIMAL(18,0) COMMENT 'Номер события',
										dep_nm STRING COMMENT 'Офис',
										loc_start_time TIMESTAMP COMMENT 'Локальное время начала обслуживания',
										loc_finish_time TIMESTAMP COMMENT 'Локальное время окончания обслуживания',
										transaction_time_sec INT COMMENT 'Продолжительность обслуживания',
										waiting_time_sec INT COMMENT 'Время ожидания',
										rndr_service_nm STRING COMMENT 'Вид операции',
										type_nm STRING COMMENT 'Тип операции',
										vip_flg TINYINT COMMENT 'Флаг ВИП',
										report_month TIMESTAMP COMMENT 'Отчетный месяц')							
COMMENT 'Первичная выборка без нормативного времени'
STORED AS PARQUET
```
Для инкремента создадим две `CTE` `last_period` которая будет проверять максимальную дату отчетного периода в витрине и `has_records` которая проверяет есть ли в витрине записи.
Далее с помощью `CROSS JOIN` тянем к первичной выборке и в `WHERE` реализуем инкремент.
```
/*Первичная выборка без нормативного времени
  Так же реализуется Инкрементальное обновление данных:
  Если в витрине нет записей - то добавляем все данные из источника
  Если в витрине есть записи - то берем данные начиная с последнего периода
  Расчет в начале месяца (1 - 3 числа), попадают данные за предыдущие полные месяца*/
INSERT INTO sbxm_hr.ees_first_sample_non_norm_time_tmp_test
WITH last_period AS (--Определяем максимальную дату отчетного месяца в витрине
                    SELECT MAX(report_dt) AS max_report_dt
                    FROM sbxm_hr.ees_client_flow_to_office_test
                    ),                    
has_records AS (--Проверка, есть ли в витрине записи
			    SELECT (COUNT(*) = 0) AS is_empty  
			    FROM sbxm_hr.ees_client_flow_to_office_test
			   )                   
SELECT
	COALESCE(ev.party_rk, ed.party_rk) AS party_global_rk,
	ev.user_login, 
	ev.event_rk, 
	ev.dep_nm,
	ev.loc_start_time, 
	ev.loc_finish_time, 
	ev.transaction_time_sec,
	ev.waiting_time_sec,
	ev.rndr_service_nm,
	xdot.type_nm,
	pgi.vip_flg,	
	LAST_DAY(ev.loc_start_time) AS report_month
FROM dm_evd.event_visit ev
LEFT JOIN dm_evd.event_rel er ON ev.event_rk = er.child_event_rk AND relationship_type_cd = 'VISIT_X_DASHBOARD'
LEFT JOIN dm_evd.event_dashboard ed ON ed.event_rk = er.parent_event_rk
LEFT JOIN dm_evd.party p ON ed.party_guid = p.abs_id AND p.party_type_cd = 'MDM_GLOBAL_IND'
LEFT JOIN dm_evd.party_global_individual pgi ON pgi.party_global_rk = p.party_rk
LEFT JOIN sbxm_hr.xref_do_operation_type xdot ON ev.rndr_service_nm = xdot.service_nm
CROSS JOIN last_period lp
CROSS JOIN has_records hr
WHERE 1 = 1 
      AND ev.loc_start_time >= DATE '2020-01-01'
      AND (
		    /*Если в витрине нет записей*/
		    (hr.is_empty AND ev.loc_start_time >= DATE '2020-01-01')
		    OR
		    /*Если в витрине есть записи, то берем данные начиная с последнего периода*/
		    (DATE_TRUNC('month', ev.loc_start_time) > DATE_TRUNC('month', lp.max_report_dt) AND 
		    DATE_TRUNC('month', ev.loc_start_time) < DATE_TRUNC('month', now()))
		   )
/
compute stats sbxm_hr.ees_first_sample_non_norm_time_tmp
```

**Пример результата:**

Представим что сегодня 03.08.2025 года. В витрине последняя дата май 2025 года, надо добавить данные за июль и июнь 2025 года, данные за первые числа августа в витрину не должны попасть.

<img width="390" height="199" alt="image" src="https://github.com/user-attachments/assets/d522b2f2-b476-49ed-a537-44712183d38f" />

Запускаем расчет первичной выборки и видим что в первичную выборку попал период с `01-06-2025` по `31-07-2025`

<img width="485" height="220" alt="image" src="https://github.com/user-attachments/assets/a95b6884-f6eb-4a14-aba4-b9824fab7630" />

Далее на основе этой выборки производятся расчеты остальных атрибутов и данные заливаются в витрину. 
