# Построение Полигонов на графике "GeoJSON на карте"

💼 Пример реального рабочего кейса: Работа с JSON в SQL

В нашей базе данных🛢️ есть таблица, в которой данные хранятся в формате JSON. 

Задача следующая🐾: написать SQL-запрос, который распарсит этот JSON и извлечет координаты, необходимые для построения карты🗺️ в Superset.

Ниже приведен пример SQL-запроса, который позволяет извлечь координаты🔵 из JSON-формата. 

```
--Шаги 
--Распарсить JSON 
--Преобразовать текст в формате WKT в геометрию ST_GeomFromText 
--Явно назначить SRID который известен с помощью ST_SetSRID функция подменяет в метаинформации данные о SRID 
--Применяем функцию ST_Transform, чтобы в столбце изменились координаты на метаинформацию которую записали 
--Вернуть текстовое представление геометрии при помощи функции ST_AsText 
--Преобразовать полученные координаты в GEOJSON
--Так как данных много, то результат в виде таблицы может не отображаться, но на графике в superset все строится и отображается.

WITH t1 AS (SELECT id, error_reason, coordinates
FROM(SELECT id,  public.ST_IsValidReason(public.st_astext(public.ST_GeomFromText(psd.json_data->'capitalConstructionObject'->'capitalConstructionObjectData'->>'coordinates'))) AS error_reason,
public.st_astext(public.st_transform(public.st_setsrid(public.ST_GeomFromText(psd.json_data->'capitalConstructionObject'->'capitalConstructionObjectData'->>'coordinates'), 10000),4326))  AS coordinates
FROM ps.documents psd
WHERE psd.json_data-> 'capitalConstructionObject'->'capitalConstructionObjectData'->>'coordinates' IS NOT NULL
AND doc_type = 'CAPITAL-CONSTRUCTION-OBJECT'
AND json_data->'capitalConstructionObject'->'capitalConstructionObjectData'->>'removed' = 'false'
AND json_data->'capitalConstructionObject'->'capitalConstructionObjectData'->>'status' IN ('01', '02','03','04','05','06')
AND json_data->'capitalConstructionObject'->'capitalConstructionObjectData'->>'functionalPurposeReport' IS NOT NULL) AS itog
WHERE error_reason = 'Valid Geometry' AND coordinates LIKE 'POLYGON%' LIMIT 10)

SELECT jsonb_pretty(
        jsonb_build_object(
        'type', 'FeatureCollection',
        'features', jsonb_agg(
        jsonb_build_object(
        'type', 'Feature',
        'geometry', public.ST_AsGeoJSON(coordinates)::jsonb,  'properties', '{}'  )))) AS geojson 
FROM t1
```

В результате получаем таблицу с строкой в формате GEOJSON в котором лежат координаты (координаты описывают полигоны, или многоугольник (Polygon), — область, ограниченная замкнутой линией. Может быть сплошной или иметь пустые области внутри. Может обозначать парк, промышленную зону, остров и т. д.). Далее эти данные будут использованы для построения графика в виде карты в Superset с целью дальнейшего анализа.

Построение карты

![image](https://github.com/user-attachments/assets/7c2fe123-a101-4c54-86ee-bf3b5f0c7184)

Если приблизить увидим POLYGON

![image](https://github.com/user-attachments/assets/a1b39934-713c-4158-b067-b9a5a47d34e6)


🔗 [Ссылка](https://postgrespro.ru/docs/postgrespro/9.5/functions-json) на доку по работе с JSON, много полезных штук

# Тестовое построение точки на графике "GeoJSON на карте" 

**SQL запрос преобразования координат точки в GEOJSON**

```
WITH t1 AS (SELECT 
public.st_astext(public.ST_GeomFromText('POINT(37.694243 55.789314)'))  AS coordinates
FROM ps.documents psd
LIMIT 1)

SELECT jsonb_pretty(
        jsonb_build_object(
        'type', 'FeatureCollection',
        'features', jsonb_agg(
        jsonb_build_object(
        'type', 'Feature',
        'geometry', public.ST_AsGeoJSON(coordinates)::jsonb,  'properties', '{}'  )))) AS geojson 
FROM t1
```

**Получаем результат**

```
{ "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates": [ 37.694243, 55.789314 ] }, "properties": "{}" } ] }
```

**Настройки графика**

![image](https://github.com/user-attachments/assets/9d1b7a8a-f695-4a8b-9268-d4b29d87d950)

![image](https://github.com/user-attachments/assets/1d17b399-2020-4369-a104-06b2ae0ceaa5)



