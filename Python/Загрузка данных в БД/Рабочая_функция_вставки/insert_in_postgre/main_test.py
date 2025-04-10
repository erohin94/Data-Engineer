import pandas as pd
from insert_in_postgresql import insert_into_hadoop, sql_query_execute
from params import *
from create_table import *




# 1.Создание таблиц в БД
for query in create_table_query_list:
    sql_query_execute(query, vk_cloud_hadoop)

#2.Вставка данных
df = pd.read_csv('C:/Users/erohi/Desktop/gazprombank/V4.1/insert_in_postgre/df_result.csv')
df_full = pd.read_csv('C:/Users/erohi/Desktop/gazprombank/V4.1/insert_in_postgre/full_resume_df.csv')

df = df.astype(object)

insert_into_hadoop(df_full, db_schema, full_resume_table, vk_cloud_hadoop)
insert_into_hadoop(df, db_schema, resume_table, vk_cloud_hadoop)