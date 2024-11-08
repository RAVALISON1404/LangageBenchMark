import json
import os

import pandas as pd

with open('PH.JSON', 'r') as file:
    data = json.load(file)

frameworks = data['frameworks']
rawData = data['rawData']

directory = 'datas/frameworks'
df = pd.DataFrame(frameworks, columns=['frameworks'])
os.makedirs(directory, exist_ok=True)
csv_file_path = os.path.join(directory, 'data.csv')
df.to_csv(csv_file_path, index=False)
for key in rawData.keys():
    directory = f'datas/{key}'
    df = pd.DataFrame()
    if 'Counts' not in key:
        for framework in rawData[key].keys():
            for items in rawData[key][framework]:
                row = {'frameworks': framework}
                row.update(items)
                df = df._append(row, ignore_index=True)
    else:
        df = pd.DataFrame(list(rawData[key].items()), columns=['frameworks', 'counts'])
    os.makedirs(directory, exist_ok=True)
    csv_file_path = os.path.join(directory, 'data.csv')
    df.to_csv(csv_file_path, index=False)

# Listes des frameworks à comparer (C# et Java)
frameworks_to_compare = ['aspcore', 'nancy', 'servicestack-v6 ', 'spring', 'javalin', 'jooby', 'micronaut', 'quarkus',
                         'ratpack', 'vertx']
for key in rawData.keys():
    data_path = f'datas/{key}/data.csv'
    data_df = pd.read_csv(data_path)
    pattern = '|'.join(frameworks_to_compare)
    filtered_df = data_df[data_df['frameworks'].str.contains(pattern, case=False, na=False)]
    filtered_df.to_csv(f'datas/{key}.csv', index=False)

df = pd.read_csv('survey_results_public.csv')

language_column = 'LanguageHaveWorkedWith'
database_column = 'DatabaseHaveWorkedWith'

language_counts = df[language_column].str.split(';').explode().value_counts().sort_values(ascending=False)

database_counts = df[database_column].str.split(';').explode().value_counts().sort_values(ascending=False)

print("Langages les plus utilisés :")
print(language_counts)

print("\nBases de données les plus utilisées :")
print(database_counts)
