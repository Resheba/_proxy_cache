from pandas import DataFrame
from json import load


with open('data.json', encoding='utf-8') as data:
    df: DataFrame = DataFrame(load(data))


df.to_sql('data', con='postgresql://postgres:postgres@localhost:5432/postgres', if_exists='replace', index=False)