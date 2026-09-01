import csv

import psycopg2

with open('data/customers_data.csv', newline='', encoding='utf-8') as file:
    customers_data = [row for row in csv.reader(file) if 'customer_id' not in row]

with open('data/employees_data.csv', newline='', encoding='utf-8') as file:
    employees_data = [row for row in csv.reader(file) if 'first_name' not in row]

with open('data/orders_data.csv', newline='', encoding='utf-8') as file:
    orders_data = [row for row in csv.reader(file) if 'order_id' not in row]

conn = psycopg2.connect(
    host='localhost',
    database='analysis',
    user='postgres',
    password='Lroberon24',
    port=5432
)

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.customers (
    customer_id char(5) PRIMARY KEY,
    company_name varchar(100) NOT NULL,
    contact_name varchar(100) NOT NULL
);
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.employees (
    employee_id serial PRIMARY KEY ,
    first_name varchar(25) NOT NULL,
    last_name varchar(35) NOT NULL,
    title varchar(100) NOT NULL,
    birth_date date NOT NULL,
    notes text
);
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.orders (
    order_id int PRIMARY KEY,
    customer_id char(5) references customers(customer_id) NOT NULL,
    employee_id  int references employees (employee_id) NOT NULL,
    order_date  date NOT NULL,
    ship_city  varchar(100) NOT NULL
);
''')

for i in customers_data:
    cur.execute('INSERT INTO public.customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s) ON CONFLICT (customer_id) DO NOTHING RETURNING *', i)

for i in employees_data:
    cur.execute('INSERT INTO public.employees (first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (employee_id) DO NOTHING RETURNING *', i)

for i in orders_data:
    cur.execute(
        'INSERT INTO public.orders (order_id,customer_id,employee_id,order_date,ship_city) VALUES (%s, %s, %s, %s,%s) ON CONFLICT (order_id) DO NOTHING  RETURNING *',
        i)

conn.commit()

cur.close()
conn.close()
