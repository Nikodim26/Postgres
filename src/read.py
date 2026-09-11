import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='demo',
    user='postgres',
    password='Lroberon24',
    port=5432
)

cur = conn.cursor()

# cur.execute("""select DISTINCT order_date from orders
#             where order_date BETWEEN '1997-11-04' and '1997-12-04'
#             order by order_date DESC
#             limit 5
#             ;""")
cur.execute("""SELECT * FROM bookings.flights
                order by flight_id asc
                limit 10
            ;""")

a = cur.fetchall()
print(len(a))


for i in a:
    print(i)

cur.close()
conn.close()
