

**SQL запрос**
```
--Шаги 
--Распарсить JSON 
--Преобразовать текст в формате WKT в геометрию ST_GeomFromText 
--Явно назначить SRID который известен с помощью ST_SetSRID функция подменяет в метаинформации данные о SRID 
--Применяем функцию ST_Transform, чтобы в столбце изменились координаты на метаинформацию которую записали 
--Вернуть текстовое представление геометрии при помощи функции ST_AsText 
--Преобразовать полученные координаты в GEOJSON
--Так как данных много, то результат в виде таблицы может не отображаться, но на графике в superset все строится и отображается.
```
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
