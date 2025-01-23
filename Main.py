import sqlite3
from random import random

from faker import Faker

fake = Faker(locale='uk_UA')
con = sqlite3.connect('student_records.db')

c = con.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS students (
student_id INTEGER PRIMARY KEY,
first_name TEXT, 
last_name TEXT, 
birth_date DATE, 
major TEXT
)
''')

major_list = ['Computer Science',
              'Computer Science',
              'Computer Science',
              'Tourism',
              'Tourism']

# записуємо данні в таблицю студенти
major_iterator = iter(major_list)
for _ in range(10):
    current_major = next(major_iterator, None)

    if current_major is None:
        major_iterator = iter(major_list)
        current_major = next(major_iterator)
    c.execute("INSERT INTO students (first_name, last_name, birth_date, major) VALUES(?,?,?,?)",
              (fake.first_name(), fake.last_name(), fake.date(), current_major))

c.execute('''
CREATE TABLE IF NOT EXISTS courses(
course_id INTEGER PRIMARY KEY,
course_name INTEGER, 
credits INTEGER
)
''')

# записуємо дані в таблицю курси
for i in range(10):
    c.execute("INSERT INTO courses (course_name, credits) VALUES (?, ?)",
              (fake.random_int(1, 4), fake.random_int(1, 5)))

c.execute('''
CREATE TABLE IF NOT EXISTS Request_1 (
student_id INTEGER PRIMARY KEY,
first_name TEXT, 
last_name TEXT, 
birth_date DATE, 
major TEXT
)                   
''')

c.execute("INSERT INTO Request_1 SELECT * FROM students WHERE major = 'Computer Science'")
con.commit()

c.execute('''
CREATE TABLE IF NOT EXISTS Request_2 (
course_id INTEGER PRIMARY KEY,
course_name INTEGER, 
credits INTEGER
)                   
''')

c.execute("INSERT INTO Request_2 SELECT * FROM courses WHERE credits > 3")
con.commit()

# Оновлення інформації про студента з ID 3

c.execute('UPDATE students SET major = ? WHERE student_id = ?', ('Data Engineering', '3'))
con.commit()

# Видалення запису з ID 2 в таблиці курси

c.execute('DELETE FROM courses WHERE course_id = ?', (2,))

# Створення таблиці enrollments з зовнішніми ключами
c.execute('''
CREATE TABLE IF NOT EXISTS enrollments (
enrollment_id INTEGER PRIMARY KEY,
student_id INTEGER,
course_id INTEGER,
enrollment_date DATE,
FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
)
''')

# Заповнення таблиці enrollments випадковими даними
for _ in range(10):
    student_id = fake.random_int(1, 10)
    course_id = fake.random_int(1, 10)
    enrollment_date = fake.date_this_decade()
    c.execute("INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (?, ?, ?)",
              (student_id, course_id, enrollment_date))

con.commit()
con.close()