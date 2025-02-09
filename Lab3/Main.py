import pandas as pd

file_path = "C:\\Users\\user\\Downloads\\zfpo_rivne_region.xlsx"

df = pd.read_excel(file_path, sheet_name="Здобувачі")

print(df.head(10))

#2
suma = df['Здобувачів'].sum()
print("\nЗагальна кількість здобувачів у всіх закладах освіти:", suma)

total_students = df.groupby("Фінансування")["Здобувачів"].sum()
print("\nЗагальна кількість здобувачів для кожного типу фінансування\n", total_students)

students = df.groupby('Освітній ступінь')['Здобувачів'].sum()
print('\nКількість здобувачів за кожним освітнім ступенем\n', students)

major = df.groupby('Спеціальність')['Здобувачів'].max().nlargest(3)
print("\nТри спеціальності, які мають найбільше кількість здобувачів:\n", major)

3

filtered_df = df[df['Освітній ступінь'] == 'Фаховий молодший бакалавр']

print(filtered_df.head(10))

filtered_institutions = df[df['Здобувачів'] > 50]

print(filtered_institutions[['Заклад освіти', 'Здобувачів']])

filtered_data = df[(df['Фінансування'] == 'Контракт') & (df['Здобувачів'] > 10)]

print(filtered_data.head(10))

4

df['Тип/Фінансування'] = df['Тип закладу освіти'].astype(str) + '/' + df['Фінансування'].astype(str)

print(df[['Тип закладу освіти', 'Фінансування', 'Тип/Фінансування']].head())

df['Рентабельність'] = df.apply(lambda row: row['Здобувачів'] * 17000 if row['Фінансування'] == 'Контракт' else None, axis=1)

print(df[['Фінансування', 'Здобувачів', 'Рентабельність']].head())

filtered_data = df[df['Фінансування'] == 'Контракт']

filtered_data.to_excel("filtered_data_contract.xlsx", index=False)
